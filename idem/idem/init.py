# The order of the sequence that needs to be implemented:
# Start with a single sls file, just like you started with salt
# Stub out the routines around gathering the initial sls file
# Just use a yaml renderer and get it to where we can manage some basic
# includes to drive to highdata

# Then we can start to fill out renderers while at the same time
# deepening the compiler

# Import python libs
import asyncio

__func_alias__ = {'compile_': 'compile'}


def __init__(hub):
    hub.pop.sub.load_subdirs(hub.idem)
    hub.idem.RUNS = {}
    hub.pop.sub.add('idem.sls')
    hub.pop.sub.add(dyne_name='rend')
    hub.pop.sub.add(dyne_name='output')
    hub.pop.sub.add(dyne_name='exec')
    hub.pop.sub.load_subdirs(hub.exec, recurse=True)
    hub.pop.sub.add(dyne_name='states')
    hub.pop.sub.load_subdirs(hub.states, recurse=True)
    hub.idem.init.req_map()


def req_map(hub):
    '''
    Gather the requisite restrtrictions and populate the requisite behavior map
    '''
    rmap = {}
    for mod in hub.idem.req:
        if mod.__sub_name__ == 'init':
            continue
        if hasattr(mod, 'define'):
            rmap[mod.__sub_name__] = mod.define()
    hub.idem.RMAP = rmap


def cli(hub):
    '''
    Execute a single idem run from the cli
    '''
    hub.pop.conf.integrate(['idem'], cli='idem', roots=True)
    hub.pop.loop.start(
            hub.idem.init.apply(
                'cli',
                hub.OPT['idem']['sls_sources'],
                hub.OPT['idem']['render'],
                hub.OPT['idem']['runtime'],
                ['states'],
                hub.OPT['idem']['cache_dir'],
                hub.OPT['idem']['sls'],
                )
            )
    # TODO Add outputter support here
    import pprint
    pprint.pprint(hub.idem.RUNS['cli']['running'])


def create(hub, name, sls_sources, render, runtime, subs, cache_dir):
    '''
    Create a new instance to execute against
    '''
    hub.idem.RUNS[name] = {
            'sls_sources': sls_sources,
            'render': render,
            'runtime': runtime,
            'subs': subs,
            'cache_dir': cache_dir,
            'states': {},
            }


async def apply(hub, name, sls_sources, render, runtime, subs, cache_dir, sls):
    '''
    Run idem!
    '''
    hub.idem.init.create(name, sls_sources, render, runtime, subs, cache_dir)
    # Get the sls file
    # render it
    # compile high data to "new" low data (bypass keyword issues)
    # Run the low data using act/idem
    await hub.idem.resolve.gather(name, *sls)
    lowdata = await hub.idem.init.compile(name)
    ret = await hub.idem.run.init.start(name)


async def compile_(hub, name):
    '''
    Compile the data defined in the given run name
    '''
    for mod in hub.idem.compiler:
        if hasattr(mod, 'stage'):
            ret = mod.stage(name)
            if asyncio.iscoroutine(ret):
                await ret
