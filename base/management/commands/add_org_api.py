import json
import requests
from django.core.management.base import BaseCommand
from Bio import SeqIO
from BCBio import GFF


class Command(BaseCommand):
    """
    A manage.py command that creates an organism, refseq, and genes
    based on input data, via API.
    """
    help = 'Adds new organism and its features'

    def auth(self):
        r = requests.post(self.url_base + 'api-token-auth/', data=json.load(self.creds)['cacao'])
        self.headers = {
            'AUthorization': 'JWT ' + r.json()['token']
        }

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help="URL of CACAO API")
        parser.add_argument('creds', type=open, help="File containing CACAO credentials")
        parser.add_argument('organism_name', type=str)
        parser.add_argument('taxon', type=str)
        parser.add_argument('ebi_id', type=str)
        parser.add_argument('gff3', type=open)
        parser.add_argument('fasta', type=open)

    def post(self, url, data):
        if not hasattr(self, 'headers'):
            self.auth()

        return requests.post(
            self.url_base + url,
            data=data,
            headers=self.headers
        ).json()

    def handle(self, *args, **options):
        # Setup things required for authentication.
        self.url_base = options['url']
        self.creds = options['creds']

        organism = self.post('organisms/', dict(
            common_name=options['organism_name'],
            taxon=options['taxon'],
            ebi_id=options['ebi_id']
        ))

        refseqs = {}
        for record in SeqIO.parse(options['fasta'], "fasta"):
            refseq = self.post('refseq/', dict( # noqa
                name=record.id,
                length=len(record.seq),
                organism=organism['id'],
            ))
            refseqs[record.id] = refseq

        for rec in GFF.parse(options['gff3']):
            # rs = RefSeq.objects.get(name=rec.id, organism=organism)
            rs = refseqs[rec.id]
            for feat in rec.features:
                if feat.type != 'gene':
                    continue

                self.post('genes/', {
                    "start": int(feat.location.start),
                    "end": int(feat.location.end),
                    "strand": int(feat.location.strand),
                    "refseq": rs['id'],
                    "db_object_id": feat.id,
                    "db_object_symbol": feat.id,
                    "db_object_name": "",
                    "db_object_synonym": "",
                    "db_object_type": "protein",
                    "gene_product_id": "",
                })
