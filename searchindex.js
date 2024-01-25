Search.setIndex({"docnames": ["api/explicit", "installation", "intro", "tutorials/csdl", "tutorials/explicit_disciplines", "tutorials/implicit_disciplines", "tutorials/openmdao", "tutorials/quickstart", "tutorials/units"], "filenames": ["api/explicit.md", "installation.md", "intro.md", "tutorials/csdl.md", "tutorials/explicit_disciplines.md", "tutorials/implicit_disciplines.md", "tutorials/openmdao.md", "tutorials/quickstart.md", "tutorials/units.md"], "titles": ["Explicit Discipline", "Installation", "Philote-Python", "Calling Philote Disciplines from CSDL", "Creating Explicit Disciplines", "Creating Implicit Disciplines", "Calling Philote Disciplines from OpenMDAO", "Quick Start", "Unit Definitions"], "terms": {"philot": [1, 4, 7, 8], "python": [1, 4, 7, 8], "pure": [1, 4], "librari": [1, 7, 8], "howev": [1, 4, 7, 8], "process": 1, "few": [1, 7], "extra": 1, "step": [1, 7], "grpc": [1, 7], "protobuf": 1, "must": [1, 4, 7], "first": [1, 4, 7], "The": [1, 4, 7, 8], "follow": 1, "tool": 1, "grpcio": 1, "protoletariat": 1, "importlib": 1, "resourc": 1, "addition": 1, "depend": 1, "ar": [1, 4, 7, 8], "mdo": [1, 7], "automat": 1, "dure": 1, "numpi": [1, 7], "two": [1, 4, 7], "make": 1, "sure": 1, "If": 1, "thei": [1, 4], "can": [1, 4, 7], "us": [1, 4, 8], "pip": 1, "note": [1, 8], "complet": [1, 3, 4, 7], "without": [1, 4], "unlik": 1, "other": [1, 8], "them": [1, 4], "packag": 1, "build": 1, "file": 1, "thi": [1, 3, 4, 6, 7, 8], "done": 1, "run": [1, 4, 7], "from": [1, 2, 4, 7, 8], "repositori": 1, "directori": 1, "setup": [1, 7], "py": [1, 7], "compile_proto": 1, "onc": 1, "successfulli": 1, "e": [1, 7, 8], "develop": [1, 7], "instal": 2, "quick": [2, 4], "creat": [2, 7], "explicit": [2, 7], "disciplin": 2, "implicit": 2, "unit": [2, 4, 7], "definit": [2, 4], "call": [2, 4], "featur": 3, "work": [3, 4, 6, 7], "progress": [3, 6], "yet": 3, "start": 4, "guid": [4, 7], "introduc": 4, "elabor": 4, "how": [4, 7], "In": [4, 7], "section": [4, 7], "we": [4, 7], "cover": 4, "basic": [4, 7], "implement": [4, 7], "similar": [4, 7], "wai": [4, 7], "openmdao": [4, 7, 8], "class": [4, 7], "inherit": [4, 7], "base": [4, 7, 8], "special": [4, 7], "some": [4, 7], "method": [4, 7], "calcul": [4, 7], "want": [4, 7], "To": [4, 7], "illustr": [4, 7], "let": [4, 7], "take": [4, 7], "look": [4, 7], "simpl": [4, 7], "paraboloid": [4, 7], "problem": [4, 7], "same": [4, 7], "document": [4, 6, 7, 8], "one": 4, "begin": [4, 7], "align": [4, 7], "f": [4, 7, 8], "x": [4, 7], "y": [4, 7, 8], "3": [4, 7, 8], "2": [4, 7, 8], "4": [4, 7, 8], "end": [4, 7], "execut": [4, 7], "equat": [4, 7], "explicitdisciplin": [4, 7], "provid": [4, 7], "member": [4, 7], "overload": 4, "desir": 4, "most": [4, 7], "common": [4, 8], "need": [4, 7], "setup_parti": [4, 7], "case": [4, 7], "offer": [4, 7], "deriv": [4, 8], "compute_parti": [4, 7], "import": [4, 7], "gener": [4, 7], "pm": 4, "pmdo": [4, 7], "def": [4, 7], "self": [4, 7], "add_input": [4, 7], "shape": [4, 7], "1": [4, 7, 8], "m": [4, 7, 8], "add_output": [4, 7], "f_xy": [4, 7], "exist": 4, "defin": [4, 7, 8], "input": [4, 7], "output": [4, 7], "purpos": [4, 7], "borrow": 4, "workflow": [4, 7], "which": [4, 7], "oper": [4, 7], "both": [4, 7], "here": [4, 7, 8], "each": 4, "scalar": 4, "meter": 4, "physic": 4, "mean": 4, "demonstr": [4, 7], "furthermor": 4, "wa": 4, "squar": [4, 8], "while": [4, 7], "partial": [4, 7], "within": 4, "usual": 4, "good": 4, "practic": 4, "separ": [4, 7], "behind": 4, "scene": 4, "back": 4, "so": [4, 7], "actual": 4, "differ": [4, 8], "where": 4, "variabl": [4, 7], "mai": [4, 7], "have": [4, 7], "organiz": 4, "benefit": 4, "an": 4, "respect": [4, 7], "declare_parti": [4, 7], "invok": 4, "0": [4, 7, 8], "later": 4, "pass": [4, 7], "server": 4, "dictionari": [4, 7], "name": [4, 7, 8], "kei": [4, 7], "6": [4, 7, 8], "8": [4, 7, 8], "entir": 4, "code": [4, 7], "list": [4, 8], "philote_mdo": [4, 7], "dimension": [4, 7], "exampl": [4, 7], "current": [6, 8], "interact": 7, "might": 7, "seem": 7, "difficult": 7, "when": 7, "out": 7, "help": 7, "abstract": 7, "awai": 7, "bit": 7, "intend": 7, "familiar": 7, "you": 7, "principl": 7, "standard": [7, 8], "get": 7, "attempt": 7, "user": 7, "friendli": 7, "possibl": 7, "like": [7, 8], "understand": 7, "multidisciplinari": 7, "design": 7, "optim": 7, "necessari": 7, "g": [7, 8], "what": 7, "etc": 7, "befor": [7, 8], "closer": 7, "attach": 7, "comput": 7, "declar": 7, "discuss": 7, "For": 7, "time": [7, 8], "being": 7, "skip": [7, 8], "over": 7, "function": 7, "do": 7, "detail": 7, "now": 7, "previou": 7, "serv": 7, "aspect": 7, "focu": 7, "field": [7, 8], "rather": 7, "than": 7, "commun": 7, "becaus": 7, "channel": 7, "concurr": 7, "futur": 7, "threadpoolexecutor": 7, "max_work": 7, "10": [7, 8], "next": 7, "explicitserv": 7, "attach_to_serv": 7, "final": 7, "port": 7, "open": 7, "network": 7, "add_insecure_port": 7, "50051": 7, "print": 7, "listen": 7, "wait_for_termin": 7, "wait": 7, "termin": 7, "signal": 7, "ctrl": 7, "c": [7, 8], "kill": 7, "unix": 7, "system": [7, 8], "longer": 7, "insecur": 7, "product": 7, "environ": 7, "should": [7, 8], "alwai": 7, "encrypt": 7, "traffic": 7, "minim": 7, "secur": 7, "vulner": 7, "third": 7, "parti": 7, "snoop": 7, "data": 7, "exchang": 7, "present": 7, "tutori": 7, "abov": 7, "snippet": 7, "were": 7, "taken": [7, 8], "slightli": 7, "order": 7, "didact": 7, "full": 7, "paraboloid_explicit": 7, "querri": 7, "number": [7, 8], "rang": 7, "csdl": 7, "compon": 7, "under": [7, 8], "hood": 7, "despit": 7, "fulli": 7, "abl": 7, "scientif": 7, "probabl": 7, "realist": 7, "framework": 7, "initi": 7, "np": 7, "explicitcli": 7, "insecure_channel": 7, "localhost": 7, "disclaim": 7, "appli": 7, "It": 7, "recommend": 7, "all": 7, "connect": 7, "tempt": 7, "just": 7, "evalu": 7, "point": 7, "hold": 7, "your": 7, "hors": 7, "There": 7, "mandatori": 7, "ensur": 7, "proper": 7, "behavior": 7, "sync": 7, "stream": 7, "option": 7, "between": 7, "happen": 7, "found": 7, "set": 7, "transfer": 7, "send_stream_opt": 7, "after": 7, "meta": 7, "retriev": 7, "run_setup": 7, "get_variable_definit": 7, "get_partials_definit": 7, "readi": 7, "arrai": 7, "size": 7, "run_comput": 7, "script": 7, "congratul": 7, "paraboloid_cli": 7, "keep": 7, "mind": 7, "requir": 7, "best": 7, "machin": 7, "remot": 7, "appropri": 7, "manag": 7, "permiss": 7, "mani": 7, "issu": 7, "avoid": [7, 8], "s": 8, "overlap": 8, "main": 8, "lack": 8, "cannot": 8, "specifi": 8, "none": 8, "type": 8, "instead": 8, "unitless": 8, "licens": 8, "apach": 8, "default": 8, "much": 8, "http": 8, "www": 8, "bipm": 8, "org": 8, "util": 8, "pdf": 8, "si_brochure_8_en": 8, "prefix": 8, "string": 8, "float": 8, "multipli": 8, "comment": 8, "si": 8, "e24": 8, "z": 8, "e21": 8, "e18": 8, "p": 8, "e15": 8, "t": 8, "e12": 8, "e9": 8, "e6": 8, "k": 8, "e3": 8, "h": 8, "e2": 8, "da": 8, "e1": 8, "d": 8, "u": 8, "n": 8, "9": 8, "12": 8, "15": 8, "18": 8, "21": 8, "24": 8, "iec": 8, "ei": 8, "1152921504606846976": 8, "60": 8, "pi": 8, "1125899906842624": 8, "50": 8, "ti": 8, "1099511627776": 8, "40": 8, "gi": 8, "1073741824": 8, "30": 8, "mi": 8, "1048576": 8, "20": 8, "ki": 8, "1024": 8, "base_unit": 8, "quantiti": 8, "length": 8, "mass": 8, "kg": 8, "A": 8, "temperatur": 8, "amount": 8, "mol": 8, "luminous_intens": 8, "cd": 8, "tabl": 8, "angl": 8, "rad": 8, "solid_angl": 8, "sr": 8, "monei": 8, "usd": 8, "passeng": 8, "pax": 8, "digital_data": 8, "byte": 8, "express": 8, "OR": 8, "factor": 8, "offset": 8, "reserv": 8, "word": 8, "inch": 8, "match": 8, "check": 8, "except": 8, "avail": 8, "predefin": 8, "constant": 8, "1000": 8, "gram": 8, "hz": 8, "hertz": 8, "newton": 8, "pa": 8, "pascal": 8, "j": 8, "joul": 8, "w": 8, "watt": 8, "coulomb": 8, "v": 8, "volt": 8, "farad": 8, "ohm": 8, "siemen": 8, "wb": 8, "weber": 8, "tesla": 8, "henri": 8, "degc": 8, "273": 8, "degre": 8, "celsiu": 8, "lm": 8, "lumen": 8, "lx": 8, "lux": 8, "bq": 8, "becquerel": 8, "gy": 8, "grai": 8, "sv": 8, "sievert": 8, "kat": 8, "katal": 8, "non": 8, "min": 8, "minut": 8, "3600": 8, "hour": 8, "86400": 8, "dai": 8, "deg": 8, "180": 8, "arc_minut": 8, "arc": 8, "arc_second": 8, "second": 8, "ha": 8, "1e4": 8, "hectar": 8, "l": 8, "1e": 8, "liter": 8, "1e3": 8, "tonn": 8, "metric": 8, "ton": 8, "7": 8, "60217653e": 8, "19": 8, "elementari": 8, "charg": 8, "ev": 8, "electron": 8, "66053886e": 8, "27": 8, "dalton": 8, "unifi": 8, "atom": 8, "ua": 8, "49597870700e11": 8, "astronom": 8, "au": 8, "c0": 8, "299792458": 8, "speed": 8, "light": 8, "vacuum": 8, "hbar": 8, "05457168e": 8, "34": 8, "reduc": 8, "planck": 8, "me": 8, "1093826e": 8, "31": 8, "a0": 8, "5291772108e": 8, "bohr": 8, "radiu": 8, "eh": 8, "35974417e": 8, "hartre": 8, "energi": 8, "bar": 8, "e5": 8, "pressur": 8, "ang": 8, "angstrom": 8, "nm": 8, "852e3": 8, "nautic": 8, "mile": 8, "b": 8, "28": 8, "barn": 8, "kn": 8, "knot": 8, "erg": 8, "dyn": 8, "5": 8, "dyne": 8, "pois": 8, "dynam": 8, "viscos": 8, "st": 8, "stoke": 8, "kinemat": 8, "sb": 8, "e4": 8, "stilb": 8, "lumin": 8, "ph": 8, "phot": 8, "illumin": 8, "gal": 8, "due": 8, "confus": 8, "volum": 8, "mx": 8, "maxwel": 8, "magnet": 8, "flux": 8, "renam": 8, "gauss": 8, "acceler": 8, "densiti": 8, "oe": 8, "oerst": 8, "backward": 8, "compat": 8, "degk": 8, "kelvin": 8, "nmi": 8, "54e": 8, "ft": 8, "3048": 8, "foot": 8, "609344e3": 8, "statut": 8, "ly": 8, "365": 8, "25": 8, "year": 8, "pc": 8, "648000": 8, "parsec": 8, "oz": 8, "349523125": 8, "ounc": 8, "lb": 8, "16": 8, "pound": 8, "lbm": 8, "2000": 8, "short": 8, "slug": 8, "14": 8, "5939029": 8, "wk": 8, "week": 8, "242199": 8, "yr": 8, "mo": 8, "month": 8, "degr": 8, "rankin": 8, "degf": 8, "459": 8, "67": 8, "fahrenheit": 8, "tsp": 8, "92892159375e": 8, "teaspoon": 8, "tbsp": 8, "tablespoon": 8, "floz": 8, "fluid": 8, "cup": 8, "pt": 8, "pint": 8, "qt": 8, "quart": 8, "galu": 8, "785411": 8, "gallon": 8, "galuk": 8, "54609": 8, "miscellan": 8, "lbf": 8, "44822162": 8, "forc": 8, "rev": 8, "revolut": 8, "rpm": 8, "rp": 8, "cal": 8, "184": 8, "thermochem": 8, "calori": 8, "cali": 8, "1868": 8, "intern": 8, "btu": 8, "1055": 8, "05585262": 8, "british": 8, "thermal": 8, "acr": 8, "640": 8, "hp": 8, "745": 8, "horsepow": 8, "atm": 8, "101325": 8, "atmospher": 8, "torr": 8, "760": 8, "mm": 8, "mercuri": 8, "psi": 8, "6894": 8, "75729317": 8, "per": 8, "psf": 8, "144": 8, "mu0": 8, "permeabl": 8, "eps0": 8, "permitt": 8, "grav": 8, "67259e": 8, "11": 8, "univers": 8, "gravit": 8, "nav": 8, "0221367e23": 8, "avagadro": 8, "r": 8, "31424": 8, "ga": 8, "v0": 8, "24136": 8, "ideal": 8, "mp": 8, "672614e": 8, "proton": 8, "rest": 8, "mn": 8, "674920e": 8, "neutron": 8, "sigma": 8, "66961e": 8, "stefan": 8, "boltzmann": 8, "ken": 8, "380649e": 8, "23": 8, "rinfin": 8, "09737312e7": 8, "rydberg": 8, "re": 8, "817939e": 8, "classic": 8, "lambdac": 8, "4263096e": 8, "compton": 8, "wavelength": 8, "lambdap": 8, "3214409e": 8, "lambdan": 8, "3196217e": 8, "mue": 8, "284851e": 8, "moment": 8, "mup": 8, "4106203e": 8, "26": 8, "mub": 8, "274096e": 8, "magneton": 8, "mun": 8, "050951e": 8, "nuclear": 8, "gammap": 8, "6751270e8": 8, "gyromagnet": 8, "ratio": 8, "h2o": 8, "gammapc": 8, "6751965e8": 8, "correct": 8, "diamagnet": 8, "phi0": 8, "0678538e": 8, "quantum": 8, "hme": 8, "273894e": 8, "circul": 8, "percent": 8, "100": 8, "percentag": 8}, "objects": {}, "objtypes": {}, "objnames": {}, "titleterms": {"explicit": [0, 4], "disciplin": [0, 3, 4, 5, 6, 7], "instal": 1, "requir": 1, "compil": 1, "definit": [1, 8], "philot": [2, 3, 6], "python": 2, "get": 2, "start": [2, 7], "tutori": 2, "work": 2, "openmdao": [2, 6], "csdl": [2, 3], "call": [3, 6, 7], "from": [3, 6], "creat": [4, 5], "setup": 4, "function": 4, "comput": 4, "gradient": 4, "summari": 4, "implicit": 5, "quick": 7, "stand": 7, "up": 7, "an": 7, "analysi": 7, "server": 7, "us": 7, "client": 7, "potenti": 7, "pitfal": 7, "unit": 8}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 6, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.intersphinx": 1, "sphinx.ext.viewcode": 1, "sphinxcontrib.bibtex": 9, "sphinx": 56}})