# from django.shortcuts import render
from django.http import JsonResponse

def global_stats(request):
    return JsonResponse({ "featureDensity": 0.02 })

def feature_data(request):
    return JsonResponse({
        "features": [

            { "start": 123, "end": 456 },

            { "type": "mRNA", "start": 5975, "end": 9744, "score": 0.84, "strand": 1,
            "name": "au9.g1002.t1", "uniqueID": "globallyUniqueString3",
            "subfeatures": [
                { "type": "five_prime_UTR", "start": 5975, "end": 6109, "score": 0.98, "strand": 1 },
                { "type": "start_codon", "start": 6110, "end": 6112, "strand": 1, "phase": 0 },
                { "type": "CDS",         "start": 6110, "end": 6148, "score": 1, "strand": 1, "phase": 0 },
                { "type": "CDS",         "start": 6615, "end": 6683, "score": 1, "strand": 1, "phase": 0 },
                { "type": "CDS",         "start": 6758, "end": 7040, "score": 1, "strand": 1, "phase": 0 },
                { "type": "CDS",         "start": 7142, "end": 7319, "score": 1, "strand": 1, "phase": 2 },
                { "type": "CDS",         "start": 7411, "end": 7687, "score": 1, "strand": 1, "phase": 1 },
                { "type": "CDS",         "start": 7748, "end": 7850, "score": 1, "strand": 1, "phase": 0 },
                { "type": "CDS",         "start": 7953, "end": 8098, "score": 1, "strand": 1, "phase": 2 },
                { "type": "CDS",         "start": 8166, "end": 8320, "score": 1, "strand": 1, "phase": 0 },
                { "type": "CDS",         "start": 8419, "end": 8614, "score": 1, "strand": 1, "phase": 1 },
                { "type": "CDS",         "start": 8708, "end": 8811, "score": 1, "strand": 1, "phase": 0 },
                { "type": "CDS",         "start": 8927, "end": 9239, "score": 1, "strand": 1, "phase": 1 },
                { "type": "CDS",         "start": 9414, "end": 9494, "score": 1, "strand": 1, "phase": 0 },
                { "type": "stop_codon",  "start": 9492, "end": 9494,             "strand": 1, "phase": 0 },
                { "type": "three_prime_UTR", "start": 9495, "end": 9744, "score": 0.86, "strand": 1 }
            ]
            }
        ]
        }
    )
