import warnings
import yaml

# TODO: Update docstring parameters for config variable, update docs for config_path

def af_colours(palette: str,
               colour_format = "hex",
               number_of_colours = 6,
               config_path = "./config/config.yaml"):
    """ 
    Return the chosen Analysis Function colour palette in hex or rgb
    format. For the categorical palette, this can be a chosen number of
    colours up to 6.

    Parameters
    ----------
    palette : string
        Type of palette required, with accepted values of "duo",
        "focus", "categorical", and "sequential".

    colour_format : string
        Colour format required, with accepted values of "hex" or "rgb".

    number_of_colours : int
        Number of colours required (categorical palette only). Takes
        values between 2 and 6. Returns 2 colours by default. If a
        palette other than categorical is chosen, any value passed
        is ignored.

    Raises
    ------
    ValueError
        If palette is not "categorical", "duo", "sequential", or "focus".
        Or if colour_format is not "hex" or "rgb".

    Returns
    -------
    list
        chosen_colours_list

    """
    with open(config_path) as file:
        config = yaml.load(file, Loader = yaml.BaseLoader)
    
    categorical_hex_list = config["categorical_hex_list"]
    duo_hex_list = config["duo_hex_list"]
    sequential_hex_list = config["sequential_hex_list"]
    focus_hex_list = config["focus_hex_list"]

    if palette not in ["categorical", "duo", "sequential", "focus"]:
        raise ValueError("palette value of " + palette +
             " is incorrect, must be categorical, duo, sequential, " + 
             "or focus as a string.")
    if colour_format.lower() not in ["hex", "rgb"]:
        raise ValueError("colour_format value of " + colour_format +
             " is incorrect, must be hex or rgb as a string.")
    if number_of_colours < 1:
         raise ValueError("Choose a number of colours greater than 0.")

    elif palette == "sequential":
        chosen_colours_list = sequential_colours(sequential_hex_list, colour_format)
        warnings.warn("This palette should only be used for sequential " +
                  "data. For bar charts, please ensure bars have a " +
                  "dark blue outline (hex code #12436D).",
                  stacklevel = 2)
    elif palette == "focus":
        chosen_colours_list = focus_colours(focus_hex_list, colour_format)
        warnings.warn("This palette should only be used to highlight " +
                  "specific elements to help users understand the " +
                  "information.", stacklevel = 2)

    elif palette == "duo":
        chosen_colours_list = duo_colours(duo_hex_list, colour_format)
    elif palette == "categorical":
        chosen_colours_list = categorical_colours(categorical_hex_list,
                                                  colour_format,
                                                  number_of_colours)
    
    if len(chosen_colours_list) > 4:
        warnings.warn("It is best practice to limit graphs to four " +
                      "categories where possible to avoid graphs " +
                      "becoming cluttered.",
                      stacklevel = 2)
    return chosen_colours_list


def categorical_colours(categorical_hex_list, colour_format = "hex", number_of_colours = 2):
    """ 
    Return the Analysis Function categorical colour palette as a list
    in hex or rgb format for up to 6 colours. If number_of_colours is 
    2, the function returns the duo palette.

    Parameters
    ----------
    colour_format : string
        Colour format required, with accepted values of "hex" or "rgb".

    number_of_colours : int
        Number of colours required, with accepted values between 2 and 6 inclusive.
        Returns 2 colours if no value given.

    Raises
    ------
    ValueError
        If number_of_colours is greater than 6.

    Returns
    -------
    list
        categorical_colours_list

    """

    if number_of_colours > 6:
        raise ValueError(
             "number_of_colours must not be more than 6 for the categorical palette.")
    if number_of_colours == 2:
        categorical_colours_list = duo_colours(colour_format)
        return categorical_colours_list

    elif colour_format == "hex":
        full_categorical_colours_list = categorical_hex_list
    elif colour_format == "rgb":
        full_categorical_colours_list = hex_to_rgb(categorical_hex_list)
    
    categorical_colours_list = full_categorical_colours_list[0:number_of_colours]

    return categorical_colours_list


def duo_colours(duo_hex_list, colour_format = "hex"):
    """ 
    Return the Analysis Function duo colour palette as a list of 2 
    colours in hex or rgb format. This function is also called by 
    sequential_colours() if number_of_colours is equal to 2.

    Parameters
    ----------
    colour_format : string
        Colour format required, with accepted values of "hex" or "rgb".

    Returns
    -------
    list
        duo_colours_list

    """
    
    if colour_format == "hex":
        duo_colours_list = duo_hex_list
    elif colour_format == "rgb":
        duo_colours_list = hex_to_rgb(duo_hex_list)

    return duo_colours_list


def sequential_colours(sequential_hex_list, colour_format = "hex"):
    """ 
    Return the Analysis Function sequential colour palette as a list 
    of 3 colours in hex or rgb format.

    Parameters
    ----------
    colour_format : string
        Colour format required, with accepted values of "hex" or "rgb".

    Returns
    -------
    list
        sequential_colours_list

    """
    
    if colour_format == "hex":
            sequential_colours_list = sequential_hex_list
    elif colour_format == "rgb":
            sequential_colours_list = hex_to_rgb(sequential_hex_list)
    
    return(sequential_colours_list)


def focus_colours(focus_hex_list, colour_format = "hex"):
    """ 
    Return the Analysis Function focus colour palette as a list of 2 
    colours in hex or rgb format.

    Parameters
    ----------
    colour_format : string
        Colour format required, with accepted values of "hex" or "rgb".

    Returns
    -------
    list
        focus_colours_list

    """
    
    if colour_format == "hex":
            focus_colours_list = focus_hex_list
    elif colour_format == "rgb":
            focus_colours_list = hex_to_rgb(focus_hex_list)
    
    return focus_colours_list


def hex_to_rgb(hex_colours):
    """    
    Convert a list of hex codes to a list of rgb colours.

    Parameters
    ----------
    hex_colours : list
        The hex colours to be converted as a list of strings, with or 
        without # at the beginning.

    Raises
    ------
    TypeError
        If hex_colours is not a list.

    Returns
    -------
    list
        converted_list

    """
    if type(hex_colours) != list:
        raise TypeError(
             "hex_colours must be a list.")
        
    hex_colours_new = [i.lstrip('#') for i in hex_colours]
    
    converted_list = [(tuple(int(value[i:i+2], 16) for i in (0, 2, 4))) 
                      for value in hex_colours_new]
    return converted_list