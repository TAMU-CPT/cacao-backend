from django.core.management.base import BaseCommand, CommandError
from base.models import Organism, Gene, RefSeq
from django.db import transaction
from Bio import SeqIO
from BCBio import GFF

class Command(BaseCommand):
    """
    A manage.py command that creates an organism, refseq, and genes
    based on input data.
    """
    help = 'Adds new organism and its features'

    def add_arguments(self, parser):
        parser.add_argument('organism_name', type=str)
        parser.add_argument('taxon', type=str)
        parser.add_argument('ebi_id', type=str)
        parser.add_argument('gff3', type=open)
        parser.add_argument('fasta', type=open)

    @transaction.atomic
    def handle(self, *args, **options):
        organism, created = Organism.objects.get_or_create(
                common_name=options['organism_name'],
                taxon=options['taxon'],
                ebi_id=options['ebi_id']
        )

        for record in SeqIO.parse(options['fasta'], "fasta"):
            refseq, created = RefSeq.objects.get_or_create(
                name=record.id,
                length=len(record.seq),
                organism=organism
            )

        for rec in GFF.parse(options['gff3']):
            rs = RefSeq.objects.get(name=rec.id, organism=organism)
            for feat in rec.features:
                if feat.type != 'gene':
                    continue
                gene, created = Gene.objects.get_or_create(
                    start=feat.location.start,
                    end=feat.location.end,
                    strand=feat.location.strand,
                    refseq=rs,
                    db_object_id=feat.id,
                    db_object_symbol=feat.id
                )
