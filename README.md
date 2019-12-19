# BABIP Projection Model

This repo contains the data and code to train a linear model to predict a baseball hitter's batting average on balls in play (BABIP) from peripheral statistics and notebooks demonstrating the process of assembling the data and using the model.

BABIP is a common quick check to see if a player got 'lucky' or 'unlucky', as it is largely beyond the ability of the player to control. However, some players have true talent BABIPs higher or lower than the league average of .300, so this model is useful for determining whether a player 'deserved' a high or low BABIP in a given season.

The data contains a variety of statistics from Fangraphs and Baseball Savant on standard statistics, advanced batting metrics, sprint speed, batted ball profiles, shifting, and other factors.

The model achieves a test R^2 of .54 and a MAE of .02, and should be considered valid for any recent player-season.

## Data

The data folder contains the raw data as scraped from Baseball Savant and Fangraphs and the combined and cleaned data. Any player-season with at least 300 PA from a player with a qualified season from 2014-2018 was included.

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
