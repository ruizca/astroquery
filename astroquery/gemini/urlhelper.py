"""
Utility for building URLs for accessing the Gemini Archive RESTful services.

The Gemini REST API is used behind the query calls so this utility is
used internally by those methods to construct appropriate URLs.
"""
import astropy
from astropy import units

from astroquery.utils import commons


def __handle_keyword_arg__(url, key, value):
    """ Handler function for generic keyword argument with no special handling. """
    return "%s/%s=%s" % (url, key, value)


def __handle_radius__(url, key, radius):
    """ Handler function for radius keyword with smart conversion to a degrees value """
    assert(key == "radius")
    if isinstance(radius, (int, float)):
        radius = radius * units.deg
    radius = astropy.coordinates.Angle(radius)
    if radius is not None:
        return "%s/sr=%fd" % (url, radius.deg)
    return url


def __handle_coordinates__(url, key, coordinates):
    """ Handler function for coordinates """
    assert(key == "coordinates")
    coordinates = commons.parse_coordinates(coordinates)
    if coordinates is not None:
        return "%s/ra=%f/dec=%f" % (url, coordinates.ra.deg, coordinates.dec.deg)
    return url


"""
Dictionary of custom handlers by key.

This dictionary will pass keyword/value pairs to the appropriate handler, if
they are present.  By default, the url will use `__handle_keyword_arg` to
add the key/value pair to the URL.
"""
__handlers__ = {
    "radius": __handle_radius__,
    "coordinates": __handle_coordinates__
}


class URLHelper(object):
    def __init__(self, server="https://archive.gemini.edu"):
        """ Make a URL Helper for building URLs to the Gemini Archive REST service. """
        if server is None:
            self.server = "https://archive.gemini.edu"
        elif not server.lower().startswith("http:") \
            and not server.lower().startswith("https:"):
            self.server = "https://%s" % server
        else:
            self.server = server

    def build_url(self, *args, **kwargs):
        """ Build a URL with the given args and kwargs as the query parameters.

        Parameters
        ----------
        args : list
            The arguments to be passed in the URL without a key.  Each of
            these is simply added as another component of the path in the url.
        kwargs : dict of key/value parameters for the url
            The arguments to be passed in key=value form.
        Returns
        -------
        response : `string` url to execute the query
        """

        url = "%s/jsonsummary/notengineering/NotFail" % self.server

        for arg in args:
            url = "%s/%s" % (url, arg)
        for key, value in kwargs.items():
            handler = __handlers__.get(key, __handle_keyword_arg__)
            url = handler(url, key, value)
        return url
