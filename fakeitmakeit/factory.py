import random
import re
import string

import numpy as np
import pandas as pd
from faker import Faker

import fakeitmakeit.isvalid as fmiv
import fakeitmakeit.util as fmu


def cid():
    """Generate a random 8-digit CID.

    The first digit is always 0, whereas the second digit is 1 or 2. The remaining 6
    digits are randomly generated between 0 and 9.

    Returns
    -------
    str

        Randomly generated CID.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.cid()  # doctest: +SKIP
    "01234567"

    """
    # The first digit is always 0.
    number = "0"

    # The second digit is 1 or 2.
    number += str(random.choice([1, 2]))

    # Generate the remaining 6 digits randomly between 0 and 9.
    number += "".join(str(random.randint(0, 9)) for _ in range(6))

    return number


def gender(distribution=dict(fmu.GENDERS)):
    """Generate a random gender.

    Possible gender values and their relative probabilities are passed via
    ``distribution`` - a dictionary whose keys are possible outputs and values are
    relative probablilities. The values in ``distribution`` do not have to sum to 1
    because selections will be made according to the relative weights.

    Parameters
    ----------
    distribution: dict

        Keys are possible output values and values are relative probablilities. For
        instance, ``{"male": 0.5, "female": 0.5}``.

    Returns
    -------
    str

        Randomly generated gender.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.gender()  # doctest: +SKIP
    'male'

    """
    return fmu.discrete_draw(distribution)


def title(genderval=None):
    """Generate a random title.

    If gender is provided via ``genderval``, then the title is generated
    according to it. Otherwise, the gender and accordingly the title is
    generated randomly.

    For further details, refer to:
    - https://www.grammarly.com/blog/ms-mrs-miss-difference/
    - https://publishing.rcseng.ac.uk/doi/pdf/10.1308/rcsbull.2021.141

    Parameters
    ----------
    genderval: str

        Gender.

    Returns
    -------
    str

        Randomly generated title.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.title('male')
    'Mr'
    >>> fm.title('nonbinary')
    'Mx'
    >>> fm.title()  # doctest: +SKIP
    'Mx'

    """
    genderval = genderval or gender()
    if genderval == "male":
        return "Mr"
    elif genderval == "female":
        return random.choice(["Ms", "Mrs", "Miss"])
    elif genderval == "nonbinary":
        return "Mx"
    else:
        raise ValueError(f"Invalid gender: {genderval=}")


def course(distribution=dict(fmu.COURSES)):
    """Generate a random course.

    Possible courses and their relative probabilities are passed via ``distribution``.
    It is a dictionary whose keys are possible outputs and values are relative
    probablilities. The values in ``distribution`` do not have to sum to 1 because
    selections will be made according to the relative weights.

    Parameters
    ----------
    distribution: dict

        Keys are possible outputs and values are relative probablilities. For instance,
        ``{"course1": 0.5, "course2": 0.5}``.

    Returns
    -------
    str

        Randomly generated course.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.course()  # doctest: +SKIP
    'acse'

    """
    return fmu.discrete_draw(distribution)


def country(distribution=dict(fmu.COUNTRIES), bias=None):
    """Generate a random country.

    Distribution is passed via ``distribution``. It is a dictionary whose keys are
    possible outputs and values are relative probablilities. The values in
    ``distribution`` do not have to sum to 1 because selections will be made according
    to the relative weights.

    By default, all countries are equally likely and their relative probablility is 1.
    To modify the default probablilities, pass a dictionary of countries and their
    relative probabilities via ``bias``. Internally, ``distribution |= bias`` is
    calculated.

    Parameters
    ----------
    distribution: dict

        Keys are possible outputs and values are relative probablilities.

    Returns
    -------
    str

        Randomly generated country.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.country()  # doctest: +SKIP
    'United Kingdom'
    >>> fm.country(bias={'India': 0.5, 'United Kingdom': 0.2})  # doctest: +SKIP
    'India'
    >>> fm.country(distribution={}, bias={'France': 1})
    'France'

    """
    distribution |= bias or {}
    return fmu.discrete_draw(distribution)


def username(nameval=None):
    """Generate a random username.

    The username is the combination of 2-3 lowercase letters and a random number with 2
    to 4 digits. The first letter of the username is the first letter of the first name,
    whereas the the last letter of the username is the first letter of the last name.
    Letters are followed with a random integer between 2 and 4 digits. The first digit
    of the number is never zero.

    Parameters
    ----------
    nameval: str

        Name.

    Returns
    -------
    str

        Randomly generated username.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.username('John Smith')  # doctest: +SKIP
    'jws4122'

    """
    nameval = nameval or name()

    # Get the first letter of the first name.
    first_letter, *_ = nameval.casefold().split()[0]

    # Get the first letter of the last name.
    last_letter, *_ = nameval.casefold().split()[-1]

    # Randomly decide if the string will have 2 or 3 letters.
    if random.choice([2, 3]) == 3:
        # Generate a random middle lowercase letter (can be any lowercase letter).
        middle_letter = random.choice(string.ascii_lowercase)
        letters = first_letter + middle_letter + last_letter
    else:
        letters = first_letter + last_letter

    # Generate a random number between 2 and 4 digits where the first digit is not zero.
    num_digits = random.choice([2, 3, 4])
    numbers = str(random.randint(1, 9))  # First digit is never zero
    for _ in range(num_digits - 1):
        numbers += str(random.randint(0, 9))

    return letters + numbers


def email(domainval=None):
    """Generate a random email.

    If ``domainval`` is not provided, then an email with a random domain is generated.
    Otherwise, the email is generated with the provided domain.

    Parameters
    ----------
    domainval: str

        Domain.

    Returns
    -------
    str

        Randomly generated email.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.email()  # doctest: +SKIP
    'somerandomemail@domain.com'
    >>> fm.email(domainval='myuniversity.ac.uk')  # doctest: +SKIP
    'john.doe@myuniversity.ac.uk'

    """
    fake = Faker()
    domain = domainval or fake.domain_name()
    return f"{fake.user_name()}@{domain}"


def name(genderval=None, countryval=None):
    """Generate a random name.

    This function uses Faker to generate a random name. Depending on the ``countryval``
    and ``genderval`` parameters, the name is generated according to the locale and by
    calling the appropriate method from ``Faker``. Otherwise, the name with the default
    ``Faker`` locale is returned.

    Parameters
    ----------
    genderval: str

        Gender.

    countryval: str

        Country.

    Returns
    -------
    str

        Randomly generated name.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.name()  # doctest: +SKIP
    'John Smith'
    >>> fm.name(countryval='China')  # doctest: +SKIP
    'Zhang San'
    >>> fm.name(genderval='female', countryval='Germany')  # doctest: +SKIP
    'Anna Schmidt'

    """
    locale = fmu.COUNTRY_LOCALE.get(countryval, None)
    fake = Faker(locale)

    # Romanized is available only for some countries.
    if hasattr(fake, "romanized_name"):
        res = fake.romanized_name()
    else:
        # Depending on the gender, we call the appropriate method from Faker.
        method = f"name_{genderval}" if genderval is not None else "name"

        # Not all countries have names for different genders.
        try:
            res = getattr(fake, method)()
        except AttributeError:
            res = fake.name()

        # Remove suffixes and prefixes - Mr, PhD, words with dots and all caps.
        # This is not exhaustive and some names might still contain some of these.
        pattern = r"\b(?:[A-Z]+\b|PhD|Dr\(a\)|,|Dr|Mr|Mrs|Ms|Miss|\w*\.\w*)"
        res = re.sub(pattern, "", res).strip()

    if fmiv.name(res):
        return res
    else:
        # If the name is not valid, then we generate a new one with default faker until
        # it passes validation.
        while not fmiv.name(res):
            res = Faker().name()

        return res


def mark(mean=65.0, stdev=6.0, pfail=0.02):
    """Generate a random mark.

    A mark between 0 and 100 is generated from a normal distribution with the given
    ``mean`` and standard deviation ``stdev``. There is ``fail_probability`` that the
    mark will be 0. Resulting mark is rounded to two decimal places.

    Parameters
    ----------
    mean: float

        Mean.

    stdev: float

        Standard deviation.

    pfail: float

        Probability that the mark will be 0.

    Returns
    -------
    float

        Randomly generated mark.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.mark(65, 10)  # doctest: +SKIP
    71

    """
    if np.random.rand() < pfail:
        # Return 0 with a probability of fail_probability
        return 0.0
    else:
        # Generate a random number from a normal distribution with the given
        # mean and standard deviation.
        number = np.random.normal(mean, stdev)
        # Clip the number to be be between 0 and 100.
        number = np.clip(number, 0, 100)
        # Round the number to two decimal places
        return round(number, 2)


def feedback():
    """Generate a random feedback.

    The feedback is generated by Faker and consists of one paragraph.

    Returns
    -------
    str

        Randomly generated feedback.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.feedback()  # doctest: +SKIP
    ...

    """
    return "\n\n".join(Faker().paragraphs(nb=1))


def student():
    """Generate a random student.

    Returns
    -------
    Student

        A dataclass containing student information.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.student()
    Student(cid=...)

    """
    # Values required for other fields.
    genderval = gender(distribution=fmu.cohort_bias.gender)
    courseval = course(distribution=fmu.cohort_bias.course)
    countryval = country(bias=fmu.cohort_bias.country_bias)
    first_name, *_, last_name = name(genderval=genderval, countryval=countryval).split()
    usernameval = username(nameval=f"{first_name} {last_name}")

    return fmu.Student(
        cid=cid(),
        gender=genderval,
        course=courseval,
        nationality=countryval,
        first_name=first_name,
        last_name=last_name,
        title=title(genderval=genderval),
        username=usernameval,
        email=email(domainval="imperial.ac.uk"),
        personal_email=email(),
        github=f"{course}-{username}",
        fee_status="home" if countryval == "United Kingdom" else "overseas",
        enrollment_status="enrolled",
        tutor=random.choice(fmu.cohort_bias.tutors),
    )


def cohort(n):
    """Generate a cohort of students.

    Parameters
    ----------
    n: int

        Number of students in the cohort.

    Returns
    -------
    pandas.DataFrame

        A dataframe containing student information.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.cohort(100)  # doctest: +SKIP
    ...

    """
    students = [student() for _ in range(n)]
    data = {
        col: [getattr(student, col) for student in students]
        for col in fmu._student_attributes
    }
    return pd.DataFrame(data)


def assignment(usernames, mean=65, sd=6, fail_probability=0.02, feedback=True):
    """Create an assignment DataFrame.

    Parameters
    ----------
    usernames: Iterable[str]

        Iterable of usernames.

    mean: float

        Mean mark.

    sd: float

        Standard deviation of marks.

    fail_probability: float

        Probability of failing.

    feedback: bool

        Whether to include feedback.

    Returns
    -------
    pandas.DataFrame

        DataFrame of usernames and marks.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> fm.assignment(["johndoe", "janedoe"], feedback=False)  # doctest: +SKIP
      username  mark
    0  johndoe  63.0
    1  janedoe  71.0

    """
    usernames = list(usernames)
    marks = [mark(mean, sd, fail_probability) for _ in range(len(usernames))]
    data = {"username": usernames, "mark": marks}

    if feedback:
        data["feedback"] = [feedback() for _ in range(len(usernames))]

    return pd.DataFrame(data)
