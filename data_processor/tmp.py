def plot_single_data(sorted_random_data):
    L = 0
    N_K = 1
    QBER = 2
    TAU_MISSES = 2
    REPETITIONS = 3
    data = list(filter(lambda x: x[L] == 5, sorted_random_data))  # only with L==expected_l
    data = list(filter(lambda x: x[QBER] == 11, data))  # only with QBER
    df = pd.DataFrame(data, columns=['L', 'NK', 'QBER', 'TAU_MISSED', 'REPETITIONS'])

    training_data = df.sample(frac=0.8)
    testing_data = df.drop(training_data.index)
    X_train = np.array(training_data['NK']).reshape(-1,1)
    Y_train = np.array(training_data['REPETITIONS']).reshape(-1,1)

    X_test = np.array(testing_data['NK']).reshape(-1,1)
    Y_test = np.array(testing_data['REPETITIONS']).reshape(-1,1)

    # regr1 = linear_model.BayesianRidge()
    # regr1.fit(X_train, Y_train)
    # Y_pred_iso = regr1.predict(X_test)
    # for i in range(10):
    #     regr = SVR(kernel="poly", degree=i)
    #     regr.fit(X_train, Y_train)
    #     Y_pred = regr.predict(X_test)
    #     plt.scatter(X_test, Y_test)
    #     plt.plot(X_test, Y_pred, color='red')
    # plt.plot(X_test, Y_pred_iso, color='yellow')
    # plt.show()
    # print(f"No. of training examples: {training_data.shape[0]}")
    # print(f"No. of testing examples: {testing_data.shape[0]}")
    # linear_regression = LinearRegression().fit(np.array(x), np.array(repetitions))
    # Y_pred = linear_regression.predict(np.array)
    # # svr_poly = SVR(kernel="poly").fit(X, Y)
    # # Y_pred = svr_poly.predict(X_test)
    # print(f'Mean squared error: {mean_squared_error(Y_test, Y_pred)}')
    # print(f'Coefficient of determination: {r2_score(Y_test, Y_pred)}')
    # return Y_pred



    # plt.scatter(x, mean_t_missed, label='mean_t_missed')
    # plt.scatter(x, max_required_reps, label='max')
    # plt.scatter(x, min_required_reps, label='min')
    # plt.scatter(x, median_required_reps, label='median')
    # plt.scatter(x, mean_required_reps, label='mean')
    # plt.scatter(x, min_required_reps, label='min')
    # plt.scatter(x, max_required_reps, label='max')
    #
    # plt.legend()
    # plt.show()
    # print('OK')


    # # sample data:
    # x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    # y = np.array([0.0, 0.8, 0.9, 0.1, -0.8, -1.0, -3.0])

    n = 9  # degree of polynomial
    p, C_p = np.polyfit(X_train.reshape(1,-1)[0], Y_train.reshape(1,-1)[0], 9, cov=True)   # C_z is estimated covariance matrix

    # Do the interpolation for plotting:
    t = np.linspace(0, 17500, 500)
    # Matrix with rows 1, t, t**2, ...:
    TT = np.vstack([t ** (n - i) for i in range(n + 1)]).T
    yi = np.dot(TT, p)  # matrix multiplication calculates the polynomial values
    C_yi = np.dot(TT, np.dot(C_p, TT.T))  # C_y = TT*C_z*TT.T
    sig_yi = np.sqrt(np.diag(C_yi))  # Standard deviations are sqrt of diagonal

    # Do the plotting:
    fg, ax = plt.subplots(1, 1)
    ax.set_title("Fit for Polynomial (degree {}) with $\pm1\sigma$-interval".format(n))
    ax.fill_between(t, yi + sig_yi, yi - sig_yi, alpha=.25)
    ax.plot(t, yi, '-')
    ax.plot(X_train, Y_train, 'ro')
    ax.axis('tight')

    fg.canvas.draw()
    plt.show()