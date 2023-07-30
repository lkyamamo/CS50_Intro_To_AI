import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    final_probability = 1

    person_gene_count = dict()
    probability_pass = [PROBS["mutation"], 0.5, 1 - PROBS["mutation"]]

    #classify gene counts
    for person in people:
        if person in one_gene:
            person_gene_count[person] = 1
        elif person in two_genes:
            person_gene_count[person] = 2
        else:
            person_gene_count[person] = 0
    
    #gene probability calculation
    for person in people:
        probability = 0
        genes = -1
        #0 genes
        if person_gene_count[person] == 0:
            genes = 0
            #go off PROBS
            if people[person]["mother"] == None:
                probability = PROBS["gene"][0]
            else:
                #calculates probability of mother and father not passing there genes
                probability = (1 - probability_pass[person_gene_count[people[person]["mother"]]]) * (1 - probability_pass[person_gene_count[people[person]["father"]]])
        
        #1 gene
        elif person_gene_count[person] == 1:
            genes = 1
            if people[person]["mother"] == None:
                probability = PROBS["gene"][1]
            else:
                #calculates probability of mother not passing and father passing plus probability of mother passing and father not passing there genes
                probability = (1 - probability_pass[person_gene_count[people[person]["mother"]]]) * (probability_pass[person_gene_count[people[person]["father"]]]) + (probability_pass[person_gene_count[people[person]["mother"]]]) * (1 - probability_pass[person_gene_count[people[person]["father"]]])
        
        #2 genes
        else:
            genes = 2
            #go off PROBS
            if people[person]["mother"] == None:
                probability = PROBS["gene"][2]
            else:
                #calculates probability of mother and father not passing there genes
                probability = (probability_pass[person_gene_count[people[person]["mother"]]]) * (probability_pass[person_gene_count[people[person]["father"]]])
        
        if person in have_trait:
            probability *= PROBS["trait"][genes][True]
        else:
            probability *= PROBS["trait"][genes][False]

        final_probability *= probability
    
    return final_probability

    #calculate does not have trait
    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities.keys():
        current = probabilities[person]
        if person in one_gene:
            current["gene"][1] += p
        elif person in two_genes:
            current["gene"][2] += p
        else:
            current["gene"][0] += p

        if person in have_trait:
            current["trait"][True] += p
        else:
            current["trait"][False] += p

    #raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        #normalize genes
        current = probabilities[person]["gene"]
        total = 0
        for value in current.values():
            total += value
        for key in current.keys():
            current[key] /= total

        #normalize traits
        current = probabilities[person]["trait"]
        total = 0
        for value in current.values():
            total += value
        for key in current.keys():
            current[key] /= total

    #raise NotImplementedError


if __name__ == "__main__":
    main()
