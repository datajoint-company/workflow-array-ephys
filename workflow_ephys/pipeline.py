import datajoint as dj
from elements_animal import subject
from elements_lab import lab
from elements_ephys import probe, ephys

from .paths import get_ephys_probe_data_dir as get_neuropixels_data_directory
from .paths import get_ks_data_dir as get_kilosort_output_directory
from .paths import get_paramset_idx as get_paramset_idx

if 'custom' not in dj.config:
    dj.config['custom'] = {}

db_prefix = dj.config['custom'].get('database.prefix', '')


# ------------- Activate "lab" and "subject" schema -------------

lab.activate(db_prefix + 'lab')

subject.activate(db_prefix + 'subject',
                 add_objects={'Source': lab.Source,
                              'Lab': lab.Lab,
                              'Protocol': lab.Protocol,
                              'User': lab.User})


@lab.schema
class SkullReference(dj.Lookup):
    definition = """
    skull_reference   : varchar(60)
    """
    contents = zip(['Bregma', 'Lambda'])


# ------------- Declare Session table -------------

schema = dj.schema(db_prefix + 'experiment')


@schema
class Session(dj.Manual):
    definition = """
    -> subject.Subject
    session_datetime: datetime
    """


# ------------- Activate "ephys" schema -------------

ephys.activate(db_prefix + 'ephys', db_prefix + 'probe', required_module=__name__)

# ------------- Add neuropixels probes -------------
for probe_type in ('neuropixels 1.0 - 3A', 'neuropixels 1.0 - 3B',
                   'neuropixels 2.0 - SS', 'neuropixels 2.0 - MS'):
    probe.ProbeType.create_neuropixels_probe(probe_type)

