import numpy as np
import sys
sys.path.append("../core")          # files from the core
import os
cwd = os.getcwd()
print(cwd)

import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing
import analysis.ml
import analysis.permutation_test
log_file = "b.simple.gender.search.log.txt"
# log_file = "school.gender.search_only.log.txt"
# log_file = "combined_school.gender.search.log.txt"
# log_file = "financial.gender.search.log.txt"
# log_file = "16blocks.gender.search.log.txt"
collection, names = converter.reader.read_log(log_file)
result = converter.reader.get_feature_vectors(collection, feat_choice='ads')
X, y, features = result[0], result[1], result[2]
analysis.statistics.print_counts(X,y)
classifier, observed_values, unit_assignments = analysis.ml.train_and_test(X, y,
                                       splittype='timed',
                                       splitfrac=0.2,
                                       nfolds=5,
                                       verbose=True)

treatment_names =   ["A (men's search)", "B (women's search)"]
topk0, topk1 = analysis.ml.print_only_top_features(classifier, features, treatment_names, feat_choice="ads")
analysis.statistics.print_frequencies(X, y, features, topk0, topk1)
import analysis.permutation_test
p_value = analysis.permutation_test.blocked_sampled_test(observed_values, unit_assignments,
                                                    analysis.statistics.correctly_classified)

analysis.statistics.print_frequencies(X, y, features, np.array(range(270)), np.array([]) )
