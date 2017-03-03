# from django.shortcuts import render
from django.http import JsonResponse
from base.models import GAF, Gene, Organism, RefSeq
import requests


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
            if gaf.go_id not in GOCACHE:
                try:
                    r = requests.get('https://cpt.tamu.edu/onto_api/%s.json' % gaf.go_id)
                    GOCACHE[gaf.go_id] = r.json()
                except Exception, e:
                    print(e)

            responseData = {
                "uniqueID": gaf.id,
                'start': gene.start,
                'end': gene.end,
                'strand': gene.strand,
                'name': 'Cacao Annotation ' + gaf.go_id,
                'go': gaf.go_id,
                'pmid': gaf.db_reference,
                'state': gaf.review_state,
            }

            for (key, value) in GOCACHE.get(gaf.go_id, {}).items():
                responseData['GO_%s' % key] = value

            data['features'].append(responseData)
    return JsonResponse(data)
