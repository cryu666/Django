from math import sqrt

import numpy as np
import pandas as pd

from .utils import convert_to_array, dissimilarity, special_sort, super_str


class SVDRecommender:
    def __init__(
        self,
        no_of_features=15,
        method="default",
    ):
        self.parameters = {"no_of_features", "method"}
        self.method = method
        self.no_of_features = no_of_features

    def get_params(self, deep=False):
        out = dict()
        for param in self.parameters:
            out[param] = getattr(self, param)

        return out

    def set_params(self, **params):

        for a in params:
            if a in self.parameters:
                setattr(self, a, params[a])
            else:
                raise AttributeError("No such attribute exists to be set")

    def create_utility_matrix(
        self, data, formatizer={"user": 0, "item": 1, "value": 2}
    ):

        itemField = formatizer["item"]
        userField = formatizer["user"]
        valueField = formatizer["value"]

        userList = data.loc[:, userField].tolist()
        itemList = data.loc[:, itemField].tolist()
        valueList = data.loc[:, valueField].tolist()

        users = list(set(data.loc[:, userField]))
        items = list(set(data.loc[:, itemField]))

        users_index = {users[i]: i for i in range(len(users))}

        pd_dict = {item: [np.nan for i in range(len(users))] for item in items}

        for i in range(0, len(data)):
            item = itemList[i]
            user = userList[i]
            value = valueList[i]

            pd_dict[item][users_index[user]] = value
            # print i

        X = pd.DataFrame(pd_dict)
        X.index = users

        users = list(X.index)
        items = list(X.columns)

        return np.array(X), users, items

    def fit(self, user_item_matrix, userList, itemList):

        self.users = list(userList)
        self.items = list(itemList)

        self.user_index = {self.users[i]: i for i in range(len(self.users))}
        self.item_index = {self.items[i]: i for i in range(len(self.items))}

        mask = np.isnan(user_item_matrix)
        masked_arr = np.ma.masked_array(user_item_matrix, mask)

        self.predMask = ~mask

        self.item_means = np.mean(masked_arr, axis=0)
        self.user_means = np.mean(masked_arr, axis=1)
        self.item_means_tiled = np.tile(self.item_means, (user_item_matrix.shape[0], 1))

        # utility matrix or ratings matrix that can be fed to svd
        self.utilMat = masked_arr.filled(self.item_means)

        # for the default method
        if self.method == "default":
            self.utilMat = self.utilMat - self.item_means_tiled

        k = self.no_of_features
        U, s, V = np.linalg.svd(self.utilMat, full_matrices=False)

        U = U[:, 0:k]
        V = V[0:k, :]
        s_root = np.diag([sqrt(s[i]) for i in range(0, k)])

        self.Usk = np.dot(U, s_root)
        self.skV = np.dot(s_root, V)
        self.UsV = np.dot(self.Usk, self.skV)

        self.UsV = self.UsV + self.item_means_tiled

    def predict(self, X, formatizer={"user": 0, "item": 1}):

        users = X.loc[:, formatizer["user"]].tolist()
        items = X.loc[:, formatizer["item"]].tolist()

        if self.method == "default":

            values = []
            for i in range(len(users)):
                user = users[i]
                item = items[i]

                if user in self.user_index:
                    if item in self.item_index:
                        values.append(
                            self.UsV[self.user_index[user], self.item_index[item]]
                        )
                    else:
                        values.append(self.user_means[self.user_index[user]])

                elif item in self.item_index and user not in self.user_index:
                    values.append(self.item_means[self.item_index[item]])

                else:
                    values.append(
                        np.mean(self.item_means) * 0.6 + np.mean(self.user_means) * 0.4
                    )

        return values

    def topN_similar(self, x, column="item", N=10, weight=True):

        out = list()

        if column == "user":
            if x not in self.user_index:
                raise Exception("Invalid user")
            else:
                for user in self.user_index:
                    if user != x:
                        # temp = dissimilarity(self.Usk[self.user_index[user],:], self.Usk[self.user_index[x],:], weighted=weight)
                        # out.append((user, temp))
                        out.append(user)
        if column == "item":
            if x not in self.item_index:
                raise Exception("Invalid item")
            else:
                for item in self.item_index:
                    if item != x:
                        # temp = dissimilarity(self.skV[:, self.item_index[item]], self.skV[:, self.item_index[x]], weighted=weight)
                        # out.append((item, temp))
                        out.append(item)

        out = special_sort(out, order="ascending")
        out = out[:N]
        return out

    def recommend(self, users_list, N=10, values=False):

        # utilMat element not zero means that element has already been
        # discovered by the user and can not be recommended
        predMat = np.ma.masked_where(self.predMask, self.UsV).filled(fill_value=-999)
        out = []

        if values == True:
            for user in users_list:
                try:
                    j = self.user_index[user]
                except:
                    raise Exception("Invalid user:", user)
                max_indices = predMat[j, :].argsort()[-N:][::-1]
                out.append(
                    [(self.items[index], predMat[j, index]) for index in max_indices]
                )

        else:
            for user in users_list:
                try:
                    j = self.user_index[user]
                except:
                    raise Exception("Invalid user:", user)
                max_indices = predMat[j, :].argsort()[-N:][::-1]
                out.append([self.items[index] for index in max_indices])

        return out
