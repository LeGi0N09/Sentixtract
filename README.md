# Sentixtract :chart_with_upwards_trend: :mag_right:

[![GitHub stars](https://img.shields.io/github/stars/LeGi0N09/Sentixtract)](https://github.com/LeGi0N09/Sentixtract/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/LeGi0N09/Sentixtract)](https://github.com/LeGi0N09/Sentixtract/network)
[![GitHub license](https://img.shields.io/github/license/LeGi0N09/Sentixtract)](https://github.com/LeGi0N09/Sentixtract/blob/main/LICENSE)

This project aims to provide easy data mining and basic sentiment analysis using various models and APIs. The application includes a dashboard that presents information about the provided services. The initial set of services includes:

1. Extract Tweets
2. Sentiment Analysis Based on COVID Model
3. Use the case of Google Perspective API
4. Extract tweets with sentiment scores

## Project Summary :clipboard:

Nowadays, sentiment analysis or opinion mining is a hot topic in machine learning. This project demonstrates a basic way of classifying tweets into positive or negative categories using LSTM as a baseline model. The project also explores how language models are related to LSTM and can produce improved results. By leveraging different features, tuning parameters, and utilizing external APIs like the Google Perspective API, the classifier's performance can be further enhanced.

## Getting Started :rocket:

To use this application locally, please follow the instructions below:

1. Clone the repository:

```bash
git clone https://github.com/LeGi0N09/Sentixtract.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Launch the application:

```bash
python app.py
```

4. Open your web browser and visit `http://localhost:5000` to access the dashboard.

## Contributing :handshake:

Contributions are welcome! If you have any ideas, suggestions, or bug fixes, please open an issue or submit a pull request.

## License :page_with_curl:

This project is licensed under the [MIT License](https://github.com/LeGi0N09/Sentixtract/blob/main/LICENSE).

## Acknowledgements :clap:

We would like to express our gratitude to the following resources:


- [TensorFlow](https://www.tensorflow.org/) for providing the LSTM model.
- [TextBlob](https://textblob.readthedocs.io/) for the sentiment analysis library.
- [Google Perspective API](https://www.perspectiveapi.com/) for the perspective analysis capabilities.

## Conclusion :raised_hands:

Sentiment analysis is a challenging task due to the complexity of the English language. While this project showcases a basic approach to tweet classification using LSTM, there are many avenues for improvement, such as feature extraction, parameter tuning, and exploring alternative classifiers. Sentiment analysis is in high demand due to its efficiency, accuracy, and speed, making it a valuable tool for businesses across various domains.

Feel free to explore the repository and leverage the provided services to extract data and analyze sentiments. Happy coding! :computer: :bar_chart:
