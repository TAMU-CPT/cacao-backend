# from django.shortcuts import render
from django.http import JsonResponse
from base.models import GAF, Gene, Organism, RefSeq
import requests
import uuid
from django.views.decorators.csrf import csrf_exempt


GOCACHE = {}


def global_stats(request):
    return JsonResponse({"featureDensity": 0.02})


def feature_data(request, name=None):
    """
    Gets all the annotations for an organism between a start and end location.
    """
    q_org = request.GET.get('organism')
    q_start = request.GET.get('start')
    q_end = request.GET.get('end')
    try:
        org = Organism.objects.get(common_name=q_org)
    except Organism.DoesNotExist:
        return JsonResponse({'error': 'No such organism'})

    try:
        refseq = RefSeq.objects.get(name=name, organism=org)
    except RefSeq.DoesNotExist:
        return JsonResponse({'error': 'No such refseq'})

    genes = Gene.objects.filter(refseq=refseq, start__lte=q_end, end__gte=q_start)
    data = {'features':[]}
    for gene in genes:
        for gaf in GAF.objects.filter(gene=gene):
            if gaf.go_id not in GOCACHE and ('CPT:' in gaf.go_id or 'GO:' in gaf.go_id):
                try:
                    r = requests.get('https://cpt.tamu.edu/onto_api/%s.json' % gaf.go_id)
                    GOCACHE[gaf.go_id] = r.json()
                except Exception, e:
                    print(e)

            pretty_printed_label = ""
            if 'CPT:' in gaf.go_id or 'GO:' in gaf.go_id:
                pretty_printed_label += "[%s] " % gaf.go_id
                pretty_printed_label += GOCACHE.get(gaf.go_id, {'name': 'GO Annotation'}).get('name', 'GO Annotation')
            else:
                pretty_printed_label = gaf.go_id

            responseData = {
                "uniqueID": gaf.id,
                'start': gene.start,
                'end': gene.end,
                'strand': gene.strand,
                'name': pretty_printed_label,
                'go': gaf.go_id,
                'pmid': gaf.db_reference,
                'state': gaf.review_state,
            }

            for (key, value) in GOCACHE.get(gaf.go_id, {}).items():
                responseData['GO_%s' % key] = value

            data['features'].append(responseData)
    return JsonResponse(data)


@csrf_exempt
def remap_to_new_build(request, name=None):
    """
    Gets all the annotations for an organism between a start and end location.
    """
    response = {'log': [], 'featureMap': {}}
    def log(data):
        response['log'].append(data)

    org_old = request.POST.get('organism_old') # Org Common Name
    org_new = request.POST.get('organism_new') # Org Common Name

    refseq_old_name = request.POST.get('refseq_old') # Refseq Name
    refseq_new_name = request.POST.get('refseq_new') # Refseq Name
    refseq_new_length = request.POST.get('refseq_length') # Refseq Name

    try:
        old_org_obj = Organism.objects.get(common_name=org_old)
    except Organism.DoesNotExist:
        return JsonResponse({'error': 'No such organism'})

    try:
        old_refseq_obj = RefSeq.objects.get(name=refseq_old_name, organism=old_org_obj)
    except RefSeq.DoesNotExist:
        return JsonResponse({'error': 'No such refseq'})

    # Create new org/refseq
    new_org_obj, new_org_obj_created = Organism.objects.get_or_create(
        common_name=org_new,
        taxon=old_org_obj.taxon,
        ebi_id=old_org_obj.ebi_id,
    )
    new_refseq_obj, new_refseq_obj_created = RefSeq.objects.get_or_create(
        name=refseq_new_name,
        length=refseq_new_length,
        organism=new_org_obj,
    )
    response['new_refseq_id'] = new_refseq_obj.id
    response['new_org_id'] = new_org_obj.id
    if new_org_obj_created:
        response['log'].append('New org created')
    if new_refseq_obj_created:
        response['log'].append('New refseq created')

    # Delete any genes attached to this "new" genome
    new_old_genes = Gene.objects.filter(refseq=new_refseq_obj)
    log('Removing %s deprecated genes' % len(new_old_genes))
    # Wipeout any genes on the new refseq and re-create
    new_old_genes.delete()

    # TODO: Validate this first.
    changes = [x.split('\t') for x in request.POST.get('changes').strip().split('\n')]
    renames = [x.split('\t') for x in request.POST.get('renames').strip().split('\n')]
    renames = {str(k.replace('-', '')).strip(): v for (k, v, _) in renames}
    changes = [
        {
            'from': {
                'id': x[0],
                'start': int(x[1]),
                'end': int(x[2]),
                'strand': x[3],
            },
            'to': {
                'id': x[4],
                'start': int(x[5]),
                'end': int(x[6]),
                'strand': x[7],
            }
        }
        for x in changes
    ]

    for change in changes:
        # Get old genes and copy them to new genes.
        to_move = Gene.objects.filter(
            refseq=old_refseq_obj,
            start__gt=change['from']['start'] - 1,
            start__lt=change['from']['end'] + 1,
            end__gt=change['from']['start'] - 1,
            end__lt=change['from']['end'] + 1,
        )
        log('Moving %s genes' % len(to_move))

        id_map_table = {}

        for obj in to_move:
            orig_obj_id = obj.id
            orig_obj_gafs = list(obj.gaf_set.all())
            # Apparently this creates a new object in DB? Neat.
            obj.id = None
            if str(orig_obj_id.hex) in renames:
                obj.id = uuid.UUID(renames[str(orig_obj_id.hex)])
                log("  Found mapped ID: %s -> %s" % (orig_obj_id, obj.id))
            else:
                log("  Could not remap %s properly" % orig_obj_id)

            obj.refseq = new_refseq_obj

            _pos_old = {'start': obj.start, 'end': obj.end, 'strand': obj.strand}
            pos = {}
            #If on the same strand
            if change['to']['strand'] == change['from']['strand']:
                pos = {
                    'start': obj.start + (change['to']['start'] - change['from']['start']),
                    'end': obj.end + (change['to']['start'] - change['from']['start']),
                    'strand': obj.strand,
                }
            # Not on the same strand
            else:
                # If used to be on PLUS
                if obj.strand > 0:
                    # Now on MINUS
                    pos = {
                        'start': change['to']['end'] - (obj.start - change['from']['start']),
                        'strand': -1,
                    }
                    # Feature is same length.
                    pos['end'] = pos['start'] - (obj.end - obj.start)
                # Used to be on MINUS
                else:
                    # Now on PLUS
                    pos = {
                        'start': change['to']['start'] + (change['from']['end'] - obj.start),
                        'strand': 1,
                    }
                    # Feature is same length.
                    pos['end'] = pos['start'] + (obj.end - obj.start)
            obj.strand = pos['strand']
            obj.start = pos['start']
            obj.end = pos['end']
            obj.save()
            response['featureMap'][orig_obj_id.hex] = obj.id.hex
            log('  Created %s [%s..%s(%s) => %s..%s(%s)]' % (str(obj), _pos_old['start'], _pos_old['end'], _pos_old['strand'], obj.start, obj.end, obj.strand))
            # Update CACAO annotations
            for gaf in orig_obj_gafs:
                # Make a new gaf
                gaf.id = None
                # Re-parent it
                gaf.gene = obj
                gaf.save()


    return JsonResponse(response)
