from django.core.management.base import BaseCommand, CommandError
from base.models import GAF
from django.db import transaction
import datetime

class Command(BaseCommand):
    help = 'Parses gaf file and creates GAF objects'

    def add_arguments(self, parser):
        parser.add_argument('gaf_file', type=open)

    @transaction.atomic
    def handle(self, *args, **options):

        gaf_keys = [
            'db', 'db_object_id', 'db_object_symbol', 'qualifier',
            'go_id', 'db_reference', 'evidence_code', 'with_or_from',
            'aspect', 'db_object_name', 'db_object_synonym', 'db_object_type',
            'taxon', 'date', 'assigned_by', 'annotation_extension', 'gene_product_id'
        ]

        for line in options['gaf_file']:
            if not line.startswith('!'):
                gaf_data = dict(zip(gaf_keys, line.strip().split('\t')))
                gaf_data['date'] = datetime.datetime.strptime(gaf_data['date'], '%Y%m%d')
                print gaf_data
                gaf_data['db'] = 'UniProtKB'
                gaf = GAF(**gaf_data)
                try:
                    gaf.save()
                except Exception, e:
                    raise CommandError(e)
