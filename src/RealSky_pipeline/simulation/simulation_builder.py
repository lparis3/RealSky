# src/model_alpha_pipeline_mp/simulation/simulation_builder.py
import time

from RealSky_pipeline.simulation.lensing_setup import build_lensing_setup
from RealSky_pipeline.simulation.image_generation import generate_images
from RealSky_pipeline.simulation.output_writer import write_simulation_output


def RS_3_collect(DM_type, Instrument, sampled_vals, RS_1_results, RS_2_results,
                  light_profile='INTERPOL', nss=True):
    """
    Computation half of the original RS_3: builds the lensing setup and
    renders images, but does NOT write anything to HDF5.

    Parameters
    ----------
    light_profile : str
        'INTERPOL' (default) or 'SERSIC'. Passed through to
        build_lensing_setup so the lens/source light model lists and
        kwargs match the chosen profile.

    Returns
    -------
    setup_results : object
        Output of build_lensing_setup; consumed by collect_simulation_output
        for things like source_x, source_y.
    image_results : object
        Output of generate_images; consumed by collect_simulation_output for
        the rendered image arrays, exposure times, SNR, etc.

    This is what worker processes call. Designed to be safe across processes:
    no shared file handles, no global state mutations, just pure computation
    given the inputs.
    """
    start3 = time.time()

    setup_results = build_lensing_setup(
        sampled_vals=sampled_vals,
        RS_1_results=RS_1_results,
        RS_2_results=RS_2_results,
        light_profile=light_profile,
    )

    image_results = generate_images(Instrument,
        setup_results=setup_results,
        RS_1_results=RS_1_results,
        RS_2_results=RS_2_results,
        nss=nss,
    )

    end3 = time.time()
    #print(f'Step 3 took {end3 - start3:.2f} secs')

    return setup_results, image_results


def RS_3(i, DM_type, Instrument, hf, timestamp,
          sampled_vals, RS_1_results, RS_2_results,
          light_profile='INTERPOL', nss=True):
    """
    Legacy single-process entrypoint, preserved so any non-parallel callers
    of RS_3 still work.

    Runs the computation via RS_3_collect, then writes results to the given
    open HDF5 file handle using the new collect+write split in output_writer.
    """
    from RealSky_pipeline.simulation.output_writer import collect_simulation_output

    setup_results, image_results = RS_3_collect(
        DM_type=DM_type,
        Instrument=Instrument,
        sampled_vals=sampled_vals,
        RS_1_results=RS_1_results,
        RS_2_results=RS_2_results,
        light_profile=light_profile,
        nss=nss,
    )

    collected = collect_simulation_output(
        i=i,
        DM_type=DM_type,
        Instrument=Instrument,
        timestamp=timestamp,
        sampled_vals=sampled_vals,
        RS_1_results=RS_1_results,
        RS_2_results=RS_2_results,
        setup_results=setup_results,
        image_results=image_results,
    )

    write_simulation_output(hf, i, collected)

    return image_results