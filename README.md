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
The optional web interface is provided by [Vortext](http://vortext.systems) [Spá](https://github.com/vortext/spa).
It can be installed by running the following commands:

```bash
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
```json
{"text": "Put the full text of a clinical trial in here"}
```

and it will return something like:

```json
{"marginalia": [
   {"title":"Random sequence generation",
    "type":"Risk of Bias",
    "description":"**Overall risk of bias prediction**: low",
    "annotations":[
       {"content":"A central pharmacy randomly assigned study medication in a 1:1 ratio using a computer-generated randomization sequence with variable-sized blocks ranging from 2 to 8 stratified by study site.",
        "uuid":"6e97f8d0-2970-11e5-b5fe-0242ac110006",
        "label":"biased"
       }, ...
```

## References
1. Marshall, I., Kuiper, J., & Wallace, B. (2015). Automating Risk of Bias Assessment for Clinical Trials. IEEE Journal of Biomedical and Health Informatics. [[doi]](http://dx.doi.org/10.1109/JBHI.2015.2431314)
2. Marshall, I. J., Kuiper, J., & Wallace, B. C. (2015). RobotReviewer: evaluation of a system for automatically assessing bias in clinical trials. Journal of the American Medical Informatics Association. [[doi]](http://dx.doi.org/10.1093/jamia/ocv044)
3. Kuiper, J., Marshall, I. J., Wallace, B. C., & Swertz, M. A. (2014). Spá: A Web-Based Viewer for Text Mining in Evidence Based Medicine. In Proceedings of the European Conference on Machine Learning and Principles and Practice of Knowledge Discovery in Databases (ECML-PKDD 2014) (Vol. 8726, pp. 452–455). Springer Berlin Heidelberg. [[doi]](http://dx.doi.org/10.1007/978-3-662-44845-8_33)
4. Marshall, I. J., Kuiper, J., & Wallace, B. C. (2014). Automating Risk of Bias Assessment for Clinical Trials. In Proceedings of the ACM Conference on Bioinformatics, Computational Biology, and Health Informatics (ACM-BCB) (pp. 88–95). ACM. [[doi]](http://dx.doi.org/10.1145/2649387.2649406)

## Licensing

Please note that this software is licensed under the AGPL license, please see the attached license file for full details. We are happy to consider requests to license the code under different terms, please contact mail@ijmarshall.com with any questions!
