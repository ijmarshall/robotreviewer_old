# RobotReviewer
Automatic extraction of data from clinical trial reports

A simple webserver written in Python which accepts a clinical trial (in plain text/JSON), and returns risk of bias judgements.

## Dependencies

RobotReviewer requires the following libraries:

    sklearn
    numpy
    scipy
    hickle
    nltk

`nltk` and `sklearn` are not used much, and will be removed in time

## Running

`python robot.py` will start a flask server running on `localhost:5000`. You can run the server in development mode by passing `DEBUG=true python robot.py` which will attempt live code reload.

## Running the Web UI
The optional web interface is provided by [Vortext](https://github.com/vortext/spa) [Spá](https://github.com/vortext/spa).
It can be installed by running the following commands:

```
git submodule update --init --recursive
cd static/scripts/spa/pdfjs
npm install
node make generic
cd -
python robot.py
```

This retrieves the front-end code and compiles pdf.js; and runs the server.

## Input/output

Send some JSON by POST to /annotate such as:

    {
        "text": "Put the full text of a clinical trial in here"
    }

and it will return something like:

    {
       'domain':'Random sequence generation',
       'justification':[
          u'They were randomly assigned,
          in a double-blind manner,
          to receive a bolus and infusion of either eptifibatide or placebo,
          in addition to standard therapy,
          for up to 72 hours (or up to 96 hours,
          if coronary intervention was performed near the end of the 72-hour period).',
          u'Randomization and Treatment\nRandomization was performed,
          in a double-blind manner,
          by coordinating centers in the United States or the Netherlands.',
          u'RESULTS\nPatients\nA total of 10,
          948      patients were randomly assigned to the study groups between November 1995 and January 1997:1487      patients to the low-dose eptifibatide group,
          4722      to the high-dose eptifibatide group,
          and 4739 to the placebo group.'
       ],
       'bias level':'LOW'
    }

## References
1. Marshall, I., Kuiper, J., & Wallace, B. (2015). Automating Risk of Bias Assessment for Clinical Trials. IEEE Journal of Biomedical and Health Informatics. [[doi]](http://dx.doi.org/10.1109/JBHI.2015.2431314)
2. Marshall, I. J., Kuiper, J., & Wallace, B. C. (2015). RobotReviewer: evaluation of a system for automatically assessing bias in clinical trials. Journal of the American Medical Informatics Association. [[doi]](http://dx.doi.org/10.1093/jamia/ocv044)

## Licensing

Please note that this software is licensed under the AGPL license, please see the attached license file for full details. We are happy to consider requests to license the code under different terms, please contact mail@ijmarshall.com with any questions!
