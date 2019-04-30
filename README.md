[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pganssle-talks/pycon-us-2019-dealing-with-datetimes/master?urlpath=lab/tree/materials)

# Dealing with Datetimes
These are the materials for the "Dealing with Datetimes" tutorial given at PyCon US 2019.

Dealing with dates and times is famously complicated. In this tutorial, you'll work through a few common datetime-handling tasks and handle some edge cases you are likely to encounter at some point in your career.

This tutorial will cover:

- Working with time zones
- Serializing and deserializing datetimes
- Datetime arithmetic
- Scheduling recurring events

The format will be a mix of short lectures and hands-on exercises.

# Getting started

The fastest way to get started is to [launch the binder for this repo](https://github.com/pganssle-talks/pycon-us-2019-dealing-with-datetimes). This is a cloud-hosted, runnable version of this repository.

## Working locally

To work locally, take the following steps:

1. Clone the repository:

    `git clone git@github.com:pganssle-talks/pycon-us-2019-dealing-with-datetimes.git`

2a. (optional, recommended) Create and activate a `virtualenv` or `conda env`:

 ```bash
 python3.7 -m virtualenv venv
 source venv/bin/activate
 ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Launch `jupyter notebook` or `jupyter lab`. The interface is very inuitive,
   but see the [Jupyter documentation](https://jupyter.org/documentation) if
   you have any trouble.

4. Navigate to the "materials" section to find the materials notebooks,
   organized into sections.

**Notes**:

1. This repository is only tested on Linux and may not work perfectly on Windows.
2. The minimum required Python version is 3.7
3. The demonstrations may not work if you do not have `tzdata` installed, even on Linux.


# License
All code is released under the Apache 2.0 license. All text is released under CC-0.

