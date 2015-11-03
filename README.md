# RobotReviewer
Automatic extraction of data from clinical trial reports

A simple webserver written in Python which accepts a clinical trial (in plain text/JSON), and returns risk of bias judgements.

The current release has a DOI: [![DOI](https://zenodo.org/badge/15498/ijmarshall/robotreviewer.svg)](https://zenodo.org/badge/latestdoi/15498/ijmarshall/robotreviewer)

## Systematic review author?

This software is the *web-service* version, meaning it's aimed at people who make systematic review software.

**For most systematic review authors, if you want to try out RobotReviewer, you'd probably be better using the demo version on our website, available [here](https://robot-reviewer.vortext.systems).** If you like it, you could email the person who maintains your systematic review software a link to this site - they might be interested in adding it.

(Alternatively, individual authors who are adept at installing unix software from the terminal are free to install this version on their own machines by following the optional 'Web UI' instructions below).

## Developers of systematic review software?

You may also use RobotReviewer free of charge, but with the following conditions:

1. You display the text, 'Risk of Bias automation by RobotReviewer ([how to cite](http://vortext.systems/robotreviewer))' on the same screen or webpage on which the RobotReviewer results (highlighted text or risk of bias judgements) are displayed.
2. For web-based tools, the text 'how to cite' should link to our website `http://vortext.systems/robotreviewer`
3. For desktop software, you should usually link to the same website. If this is not possible, you may alternately display the text and example citations from the 'How to cite RobotReviewer' section below.

## How to cite RobotReviewer

We offer RobotReviewer free of charge, but we'd be most grateful if you would cite us if you use it. We're academics, and thrive on links and citations!

Getting RobotReviewer widely used and cited helps us obtain the funding to maintain the project and make RobotReviewer better.

It also makes your methods transparent to your readers, and not least we'd love to see where RobotReviewer is used! :)

You can cite RobotReviewer as:

Marshall IJ, Kuiper J, & Wallace BC. RobotReviewer: evaluation of a system for automatically assessing bias in clinical trials. Journal of the American Medical Informatics Association 2015. [doi:10.1093/jamia/ocv044](http://dx.doi.org/10.1093/jamia/ocv044)

A BibTeX entry for LaTeX users is

    @article{RobotReviewer2015,
      title = {{RobotReviewer: evaluation of a system for automatically assessing bias in clinical trials}},
      author = {Marshall, Iain J and Kuiper, Jo\"{e}l and Wallace, Byron C},
      doi = {10.1093/jamia/ocv044},
      url = {http://dx.doi.org/10.1093/jamia/ocv044},
      journal = {Journal of the American Medical Informatics Association},
      year = {2015}
      month = jun,
      pages = {ocv044}
    }

## Dependencies

RobotReviewer requires the following libraries:

    sklearn
    numpy
    scipy
    hickle
    nltk

`nltk` and `sklearn` are not used much, and will be removed in time


    pip install numpy scipy sklearn hickle nltk

## Running

`python robot.py` will start a flask server running on `localhost:5000`. You can run the server in development mode by passing `DEBUG=true python robot.py` which will attempt live code reload.

## Running the Web UI

The optional web interface is provided by [Vortext](http://vortext.systems) [Spá](https://github.com/vortext/spa).
It can be installed by running the following commands:

```bash
git submodule update --init --recursive
python robot.py
```

This retrieves the front-end code, and runs the server.

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
        "uuid":"6e97f8d0-2970-11e5-b5fe-0242ac110006"
       }, ...
```

## Running as a Python module

We will add full python module functionality to a future relase. However, the current code can easily be called directly from existing python code as follows:

```python
import biasrobot # from the robotreviewer root directory

bot = biasrobot.BiasRobot()
text = "Put the full text of a clinical trial in here..."
annotations = bot.annotate(text)
```

Where the BiasRobot.annotate() method returns a "marginalia" dict of the same structure as the JSON example above.

## Help

Feel free to contact us on [mail@ijmarshall.com](mailto:mail@ijmarshall.com) with any questions.

## More help!

Our tech consultancy [Vortext](http://vortext.systems/) can help get RobotReviewer running on your server for you, or can provide fully-managed RobotReviewer cloud instances; [contact us](http://vortext.systems/hire-us/) for details.

## References

1. Marshall, I. J., Kuiper, J., & Wallace, B. C. (2015). RobotReviewer: evaluation of a system for automatically assessing bias in clinical trials. Journal of the American Medical Informatics Association. [[doi]](http://dx.doi.org/10.1093/jamia/ocv044)
2. Marshall, I., Kuiper, J., & Wallace, B. (2015). Automating Risk of Bias Assessment for Clinical Trials. IEEE Journal of Biomedical and Health Informatics. [[doi]](http://dx.doi.org/10.1109/JBHI.2015.2431314)
3. Kuiper, J., Marshall, I. J., Wallace, B. C., & Swertz, M. A. (2014). Spá: A Web-Based Viewer for Text Mining in Evidence Based Medicine. In Proceedings of the European Conference on Machine Learning and Principles and Practice of Knowledge Discovery in Databases (ECML-PKDD 2014) (Vol. 8726, pp. 452–455). Springer Berlin Heidelberg. [[doi]](http://dx.doi.org/10.1007/978-3-662-44845-8_33)
4. Marshall, I. J., Kuiper, J., & Wallace, B. C. (2014). Automating Risk of Bias Assessment for Clinical Trials. In Proceedings of the ACM Conference on Bioinformatics, Computational Biology, and Health Informatics (ACM-BCB) (pp. 88–95). ACM. [[doi]](http://dx.doi.org/10.1145/2649387.2649406)

## License

Copyright (c) 2015 Iain Marshall, Joël Kuiper, and Byron Wallace; All rights reserved
