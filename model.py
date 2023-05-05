# Split the data into training and testing sets
#         X_train, X_test, y_train, y_test = train_test_split(df[['color_1', 'color_2']], df['target'], test_size=0.2, random_state=42)


#         # Convert the color names into numerical values
#         color_dict = {'black': 0, 'white': 1, 'grey': 2, 'red': 3, 'blue': 4, 'green': 5, 'yellow': 6, 'purple': 7, 'pink': 8}
#         X_train = X_train.replace(color_dict)
#         X_test = X_test.replace(color_dict)

#         # Create a logistic regression model and fit it to the training data
#         model = LogisticRegression()
#         model.fit(X_train, y_train)

#         serialized_model=pickle.dumps(model)
