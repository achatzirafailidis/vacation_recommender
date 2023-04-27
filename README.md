# Vacation Recommender

### Introduction

This project was my final project for the Spiced Academy, Data Science course. The idea behind the project is to provide users with a model where they can get recommendations for vacation spots based on a prompt plus a choice of type of vacation. The user then receives a recommendation based(for the time being) on information about 100 spots. The motivation behind the project was to familiarize myself with image classification but also natural language processing(which has sparked my interest to delve deeper into NLP)

## Table of contents
* [Technologies](#technologies)
* [Data](#data) 
* [Methodology](#methodology)
* [Future Work] (#future work)

## Technologies
Project is created with:
* Streamlit
* Spacy
* Pandas
* Sklearn
* Selenium
* BeautifulSoup
	
## Data

The data used have been retrieved by Flickr and TripAdvisor, through FlickrAPI and web scrapping(Selenium and BeautifulSoup)

## Methodology

The first version of the project used images from flickr for a list of 100 locations, to classify them between sea, mountain and city. Then based on a user prompt the user input text is cleaned(first version is using only nouns) and then using spacy checked against Flickr tags for semantic similarity. For example the use of hte prompt "I would like to go hiking in nature" produced as first recommendation the Trolltunga mountain. Future iterations will remove the image classification part and will only use NLP to analyse user prompts to produce better results

## Future Work

The next iteration will use word vectors to check for semantic similarity between the user prompt and Tripadvisor reviews and use BERT based models for sentiment analysis, to exclude overly negative prompts
