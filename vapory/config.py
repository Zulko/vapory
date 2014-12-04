import os

POVRAY_BINARY = ("povray.exe" if os.name=='nt' else "povray")

GLOBAL_SCENE_SETTINGS = {
    "charset"        : "ascii",
    "adc_bailout"    : "1/255",
    "ambient_light"      : (1,1,1),
    "assumed_gamma"     : 1.0,
    "irid_wavelength"    : (0.25,0.18,0.14),
    "max_trace_level"    : 5,
    "max_intersections"  : 64,
    "mm_per_unit"        : 10,
    "number_of_waves"    : 10,
    "noise_generator"    : 2,

    "Radiosity":{
    "adc_bailout"    : 0.01,
    "always_sample"      : "off",
    "brightness"     : 1.0,
    "count"          : 35,
    "error_bound"    : 1.8,
    "gray_threshold"     : 0.0,
    "low_error_factor"   : 0.5,
    "max_sample"     : -1,
    "maximum_reuse"      : 0.2,
    "minimum_reuse"      : 0.015,
    "nearest_count"      : 5,
    "normal"         : "off" ,
    "pretrace_start"     : 0.08,
    "pretrace_end"       : 0.04,
    "recursion_limit"    : 2,
    "subsurface"     : "off"},

    "Subsurface":{
    "radiosity"      : "off",
    "samples"        : (50,50)},
}
