# from django.shortcuts import render
from django.http import JsonResponse
from base.models import GAF, Gene, Organism, RefSeq

def global_stats(request):
    return JsonResponse({ "featureDensity": 0.02 })

def feature_data(request, name=None):
    # return JsonResponse()
    print '*************'
    q_org = request.GET.get('organism')
    q_start = request.GET.get('start')
    q_end = request.GET.get('end')
    org = Organism.objects.get(common_name=q_org)
    refseq = RefSeq.objects.get(name=name, organism=org)
    genes = Gene.objects.filter(refseq=refseq, start__lte=q_end, end__gte=q_start)
    data = {'features':[]}
    for gene in genes:
        for gaf in GAF.objects.filter(gene=gene):
            data['features'].append({
                "uniqueID": gaf.id,
                'start': gene.start,
                'end': gene.end,
                'strand': gene.strand,
                'name': 'Cacao Annotation ' + gaf.go_id,
                'go': gaf.go_id,
                'pmid': gaf.db_reference,
                'state': gaf.review_state,
            })
    return JsonResponse(data)
