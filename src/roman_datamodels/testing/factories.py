"""
Factory methods that create (not necessarily realistic) nodes
that validate against their schemas.
"""
from datetime import datetime
import math
import random
import re
import secrets
import sys
import uuid

from astropy.time import Time
import numpy as np

from .. import stnode


__all__ = [
    "create_aperture",
    "create_cal_step",
    "create_coordinates",
    "create_ephemeris",
    "create_exposure",
    "create_flat_ref",
    "create_guidestar",
    "create_meta",
    "create_observation",
    "create_photometry",
    "create_pixelarea",
    "create_pointing",
    "create_program",
    "create_ref_meta",
    "create_target",
    "create_velocity_aberration",
    "create_visit",
    "create_wcsinfo",
    "create_wfi_image",
    "create_wfi_mode",
    "create_wfi_science_raw",
    "get_factory_method",
]


def _random_float(min=None, max=None):
    if min is None:
        min = sys.float_info.min
    if max is None:
        max = sys.float_info.max
    return min + (max - min) * random.random()


def _random_positive_float(max=None):
    return _random_float(min=0.0, max=max)


def _random_angle_radians():
    return _random_float(0.0, 2.0 * math.pi)


def _random_angle_degrees():
    return _random_float(0.0, 360.0)


def _random_mjd_timestamp():
    # Random timestamp between 2020-01-01 and 2030-01-01
    return _random_float(58849.0, 62502.0)


def _random_utc_timestamp():
    # Random timestamp between 2020-01-01 and 2030-01-01
    return _random_float(1577836800.0, 1893456000.0)


def _random_string_timestamp():
    return datetime.utcfromtimestamp(_random_utc_timestamp()).strftime("%Y-%m-%dT%H:%M:%S.%3f")[0:23]


def _random_string_date():
    return datetime.utcfromtimestamp(_random_utc_timestamp()).strftime("%Y-%m-%d")


def _random_string_time():
    return datetime.utcfromtimestamp(_random_utc_timestamp()).strftime("%H:%M:%S.%3f")[0:12]


def _random_astropy_time():
    return Time(_random_utc_timestamp(), format="unix")


def _random_int(min=None, max=None):
    # Assume 32-bit signed integers for now
    if min is None:
        min = -1 * 2 ** 31
    if max is None:
        max = 2 ** 31 - 1
    return random.randint(min, max)


def _random_positive_int(max=None):
    return _random_int(0, max)


def _random_choice(*args):
    return random.choice(args)


def _random_string(prefix="", max_length=None):
    if max_length is not None:
        random_length = min(16, max_length - len(prefix))
    else:
        random_length = 16

    return prefix + secrets.token_hex(random_length)


def _random_bool():
    return _random_choice(*[True, False])


def _random_array_float32(size=(4096, 4096)):
    return np.random.default_rng().random(size=size, dtype=np.float32)


def _random_array_uint16(size=(4096, 4096)):
    return np.random.randint(0, high=2**16, size=size, dtype=np.uint16)


def _random_array_uint32(size=(4096, 4096)):
    return np.random.randint(0, high=2**32, size=size, dtype=np.uint32)


def _random_exposure_type():
    return _random_choice(
        "DEFOCUS_LARGE",
        "DEFOCUS_MODERATE",
        "WFI_DARK",
        "WFI_FLAT_EXTERNAL",
        "WFI_FLAT_INTERNAL",
        "WFI_GRISM",
        "WFI_IMAGE",
        "WFI_PARALLEL",
        "WFI_PRISM",
        "WFI_RCS",
        "WFI_WFSC",
        "WFI_WIM_ACQ",
        "WFI_WIM_TRACK",
        "WFI_WSM_ACQ1",
        "WFI_WSM_ACQ2",
        "WFI_WSM_TRACK",
    )


def _random_detector():
    return _random_choice(
        "WFI01",
        "WFI02",
        "WFI03",
        "WFI04",
        "WFI05",
        "WFI06",
        "WFI07",
        "WFI08",
        "WFI09",
        "WFI10",
        "WFI11",
        "WFI12",
        "WFI13",
        "WFI14",
        "WFI15",
        "WFI16",
        "WFI17",
        "WFI18",
    )


def _random_optical_element():
    # TODO: Replace ENGINEERING with F213 once
    # https://github.com/spacetelescope/rad/issues/6 is resolved.
    return _random_choice(
        "F062",
        "F087",
        "F106",
        "F129",
        "W146",
        "F158",
        "F184",
        "GRISM",
        "PRISM",
        "DARK",
        "ENGINEERING",
    )


def create_aperture(**kwargs):
    """
    Create a dummy Aperture instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Aperture
    """
    raw = {
        "name": _random_string("Aperture name ", 40),
        "position_angle": _random_angle_degrees(),

    }
    raw.update(kwargs)

    return stnode.Aperture(raw)


def create_cal_step(**kwargs):
    """
    Create a dummy CalStep instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.CalStep
    """
    raw = {
        "flat_field": _random_choice("N/A", "COMPLETE", "SKIPPED", "INCOMPLETE"),
    }
    raw.update(kwargs)

    return stnode.CalStep(raw)


def create_coordinates(**kwargs):
    """
    Create a dummy Coordinates instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Coordinates
    """
    raw = {
        "reference_frame": "ICRS",
    }
    raw.update(kwargs)

    return stnode.Coordinates(raw)


def create_ephemeris(**kwargs):
    """
    Create a dummy Ephemeris instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Ephemeris
    """
    raw = {
        "earth_angle": _random_angle_radians(),
        "moon_angle": _random_angle_radians(),
        "time": _random_mjd_timestamp(),
        "type": _random_choice("Definitive", "Predicted"),
        "spatial_x": _random_float(),
        "spatial_y": _random_float(),
        "spatial_z": _random_float(),
        "sun_angle": _random_angle_radians(),
        "velocity_x": _random_float(),
        "velocity_y": _random_float(),
        "velocity_z": _random_float(),
    }
    raw.update(kwargs)

    return stnode.Ephemeris(raw)


def create_exposure(**kwargs):
    """
    Create a dummy Exposure instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Exposure
    """
    raw = {
        "count": _random_positive_int(),
        "data_problem": _random_bool(),
        "duration": _random_positive_float(),
        "effective_exposure_time": _random_positive_float(),
        "elapsed_exposure_time": _random_positive_float(),
        "end_time": _random_utc_timestamp(),
        "end_time_mjd": _random_mjd_timestamp(),
        "end_time_tdb": _random_mjd_timestamp(),
        "exposure_time": _random_positive_float(),
        "frame_divisor": _random_positive_int(),
        "frame_time": _random_positive_float(),
        "gain_factor": _random_positive_float(),
        "group_time": _random_positive_float(),
        "groupgap": _random_positive_int(),
        "integration_end": _random_positive_int(),
        "integration_start": _random_positive_int(),
        "integration_time": _random_positive_float(),
        "mid_time": _random_utc_timestamp(),
        "mid_time_mjd": _random_mjd_timestamp(),
        "mid_time_tdb": _random_mjd_timestamp(),
        "nframes": _random_positive_int(),
        "ngroups": _random_positive_int(),
        "nints": _random_positive_int(),
        "nresets_at_start": _random_positive_int(),
        "nsamples": _random_positive_int(),
        "sample_time": _random_positive_float(),
        "start_time": _random_utc_timestamp(),
        "start_time_eng": _random_string_time(),
        "start_time_mjd": _random_mjd_timestamp(),
        "start_time_tdb": _random_mjd_timestamp(),
        "type": _random_exposure_type(),
    }
    raw.update(kwargs)

    return stnode.Exposure(raw)


def create_ref_meta(**kwargs):
    """
    Create a dummy reference file metadata dictionary with valid
    values for attributes required by the schema (ref_common-1.0.0).

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    dict
    """
    raw = {
        "telescope": "ROMAN",
        "instrument": {
            "name": "WFI",
            "detector": _random_detector(),
            "optical_element": _random_optical_element(),
        },
        "pedigree": "DUMMY",
        "description": _random_string("Reference description "),
        "author": _random_string("Reference author "),
        "useafter": _random_astropy_time(),
    }
    raw.update(kwargs)

    return raw


def create_flat_ref(**kwargs):
    """
    Create a dummy FlatRef instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.FlatRef
    """
    raw = {
        "data": _random_array_float32(),
        # TODO: Update this to _random_array_uint16() once the schema is fixed.
        # See https://github.com/spacetelescope/rad/issues/8
        "dq": _random_array_float32(),
        "err": _random_array_float32(),
        "meta": create_ref_meta(reftype="FLAT"),
    }
    raw.update(kwargs)

    return stnode.FlatRef(raw)


def create_guidestar(**kwargs):
    """
    Create a dummy Guidestar instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Guidestar
    """
    raw = {
        "data_end": _random_mjd_timestamp(),
        "data_start": _random_mjd_timestamp(),
        "gs_acq_exec_stat": _random_string("Status ", 15),
        "gs_ctd_ux": _random_positive_float(),
        "gs_ctd_uy": _random_positive_float(),
        "gs_ctd_x": _random_positive_float(),
        "gs_ctd_y": _random_positive_float(),
        "gs_dec": _random_float(math.pi / -2.0, math.pi / 2.0),
        "gs_epoch": _random_string("Epoch ", 10),
        "gs_function_end_time": _random_string_time(),
        "gs_function_start_time": _random_string_time(),
        "gs_id": _random_string("ID ", 20),
        "gs_mag": _random_float(),
        "gs_mudec": _random_float(),
        "gs_mura": _random_float(),
        "gs_para": _random_float(),
        "gs_pcs_mode": _random_string("PCS ", 10),
        "gs_ra": _random_angle_radians(),
        "gs_start_time": _random_string_timestamp(),
        "gs_stop_time": _random_string_timestamp(),
        "gs_udec": _random_positive_float(),
        "gs_umag": _random_positive_float(),
        "gs_ura": _random_positive_float(),
        "gs_window_xsize": _random_positive_float(),
        "gs_window_xstart": _random_positive_float(),
        "gs_window_ysize": _random_positive_float(),
        "gs_window_ystart": _random_positive_float(),
    }
    raw.update(kwargs)

    return stnode.Guidestar(raw)


def create_meta(**kwargs):
    """
    Create a dummy metadata dictionary with valid values for attributes
    required by the schema (common-1.0.0).

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    dict
    """
    raw = {
        "aperture": create_aperture(),
        "cal_step": create_cal_step(),
        "coordinates": create_coordinates(),
        "date": _random_astropy_time(),
        "ephemeris": create_ephemeris(),
        "exposure": create_exposure(),
        "filename": _random_string("Filename ", 120),
        "instrument": create_wfi_mode(),
        "model_type": _random_string("Model type ", 50),
        "observation": create_observation(),
        "photometry": create_photometry(),
        "pointing": create_pointing(),
        "origin": "STSCI",
        "program": create_program(),
        "target": create_target(),
        "telescope": "ROMAN",
        "velocity_aberration": create_velocity_aberration(),
        "visit": create_visit(),
        "wcsinfo": create_wcsinfo(),
    }
    raw.update(kwargs)

    return raw


def create_observation(**kwargs):
    """
    Create a dummy Observation instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Observation
    """
    raw = {
        "activity_id": _random_string(max_length=2),
        "date": _random_string_date(),
        "date_beg": _random_string_timestamp(),
        "date_end": _random_string_timestamp(),
        "execution_plan_number": _random_string(max_length=2),
        "exposure_number": _random_string(max_length=4),
        # TODO: The schema says this is required but doesn't provide any
        # information on the datatype.  Update this once
        # https://github.com/spacetelescope/rad/issues/9 is resolved.
        "leg_number": _random_string(max_length=4),
        "ma_table_name": _random_string("MA table "),
        "obs_id": _random_string("Obs ID ", 26),
        "observation_folder": _random_string("Observation folder "),
        "observation_label": _random_string("Observation label "),
        "observation_number": _random_string(max_length=3),
        "pass_number": _random_string(max_length=3),
        "program_number": _random_string(max_length=5),
        "template": _random_string("Template ", 50),
        "time": _random_string_time(),
        "visit_group": _random_string(max_length=2),
        "visit_id": _random_string("Visit ID ", 19),
        "visit_number": _random_string(max_length=3),
    }
    raw.update(kwargs)

    return stnode.Observation(raw)


def create_photometry(**kwargs):
    """
    Create a dummy Photometry instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Photometry
    """
    raw = {
        "conversion_megajanskys": _random_positive_float(),
        "conversion_microjanskys": _random_positive_float(),
        "pixelarea_arcsecsq": _random_positive_float(),
        "pixelarea_steradians": _random_positive_float(),
    }
    raw.update(kwargs)

    return stnode.Photometry(raw)


def create_pixelarea(**kwargs):
    """
    Create a dummy Pixelarea instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Pixelarea
    """
    raw = {
        "area": _random_array_float32(),
    }
    raw.update(kwargs)

    return stnode.Pixelarea(raw)


def create_pointing(**kwargs):
    """
    Create a dummy Pointing instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Pointing
    """
    raw = {
        "dec_v1": _random_float(-90.0, 90.0),
        "pa_v3": _random_angle_degrees(),
        "ra_v1": _random_angle_degrees(),
    }
    raw.update(kwargs)

    return stnode.Pointing(raw)


def create_program(**kwargs):
    """
    Create a dummy Program instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Program
    """
    raw = {
        "category": _random_string("Cat ", 6),
        "continuation_id": _random_positive_int(),
        "pi_name": _random_string("PI name ", 100),
        "science_category": _random_string("Science category ", 100),
        "title": _random_string("Proposal title ", 100),
    }
    raw.update(kwargs)

    return stnode.Program(raw)


def create_target(**kwargs):
    """
    Create a dummy Target instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Target
    """
    raw = {
        "catalog_name": _random_string("Catalog name ", 256),
        "dec": _random_float(-90.0, 90.0),
        "dec_uncertainty": _random_positive_float(),
        "proper_motion_dec": _random_float(),
        "proper_motion_epoch": _random_string_timestamp(),
        "proper_motion_ra": _random_float(),
        "proposer_dec": _random_float(-90.0, 90.0),
        "proposer_name": _random_string("Proposer name ", 100),
        "proposer_ra": _random_angle_degrees(),
        "ra": _random_angle_degrees(),
        "ra_uncertainty": _random_positive_float(),
        "source_type": _random_choice("EXTENDED", "POINT", "UNKNOWN"),
        "source_type_apt": _random_choice("EXTENDED", "POINT", "UNKNOWN"),
        "type": _random_choice("FIXED", "MOVING", "GENERIC"),
    }
    raw.update(kwargs)

    return stnode.Target(raw)


def create_velocity_aberration(**kwargs):
    """
    Create a dummy VelocityAberration instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.VelocityAberration
    """
    raw = {
        "ra_offset": _random_float(),
        "dec_offset": _random_float(),
        "scale_factor": _random_float(),
    }
    raw.update(kwargs)

    return stnode.VelocityAberration(raw)


def create_visit(**kwargs):
    """
    Create a dummy Visit instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Visit
    """
    raw = {
        "engineering_quality": _random_choice("OK", "SUSPECT"),
        "pointing_engdb_quality": _random_choice("CALCULATED", "PLANNED"),
        "type": _random_string("Visit type ", 30),
        "start_time": _random_string_timestamp(),
        "end_time": _random_string_timestamp(),
        "status": _random_string("Status ", 15),
        "total_exposures": _random_positive_int(),
        "internal_target": _random_bool(),
    }
    raw.update(kwargs)

    return stnode.Visit(raw)


def create_wcsinfo(**kwargs):
    """
    Create a dummy Wcsinfo instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.Wcsinfo
    """
    raw = {
        "dec_ref": _random_float(-90.0, 90.0),
        "ra_ref": _random_positive_float(360.0),
        "roll_ref": _random_float(),
        "v2_ref": _random_float(),
        "v3_ref": _random_float(),
        "v3yangle": _random_float(),
        "vparity": _random_int(),
    }
    raw.update(kwargs)

    return stnode.Wcsinfo(raw)


def create_wfi_image(**kwargs):
    """
    Create a dummy WfiImage instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.WfiImage
    """
    raw = {
        "area": _random_array_float32(),
        "data": _random_array_float32(),
        "dq": _random_array_uint32(),
        "err": _random_array_float32(),
        "meta": create_meta(),
        "var_flat": _random_array_float32(),
        "var_poisson": _random_array_float32(),
        "var_rnoise": _random_array_float32(),
    }
    raw.update(kwargs)

    return stnode.WfiImage(raw)


def create_wfi_mode(**kwargs):
    """
    Create a dummy WfiMode instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.WfiMode
    """
    raw = {
        "detector": _random_detector(),
        "name": "WFI",
        "optical_element": _random_optical_element(),
    }
    raw.update(kwargs)

    return stnode.WfiMode(raw)


def create_wfi_science_raw(**kwargs):
    """
    Create a dummy WfiScienceRaw instance with valid values for attributes
    required by the schema.

    Parameters
    ----------
    **kwargs
        Additional or overridden attributes.

    Returns
    -------
    roman_datamodels.stnode.WfiScienceRaw
    """
    raw = {
        # TODO: What should this shape be?
        "data": _random_array_uint16((1, 4096, 4096, 2)),
        "meta": create_meta(),
        # TODO: What should this shape be?
        "refout": _random_array_uint16((1, 4096, 4096, 2)),
        # TODO: What should this shape be?
        "zeroframe": _random_array_uint16((1, 4096, 4096)),
    }
    raw.update(kwargs)

    return stnode.WfiScienceRaw(raw)


def _camel_case_to_snake_case(value):
    # Courtesy of https://stackoverflow.com/a/1176023
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def get_factory_method(node_class):
    """
    Get the factory method that produces instances of the
    specified class.

    Parameters
    ----------
    node_class : type
        Node class.

    Returns
    -------
    callable
    """
    method_name = "create_" + _camel_case_to_snake_case(node_class.__name__)
    if not method_name in globals():
        raise ValueError(f"Factory method not implemented for class {node_class.__name__}")
    return globals()[method_name]
