# F29 BioEntity
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

General utilities to work with HPO and MONDO ontologies including disease, phenotype and gene annotations.

## BioGenes Methods

### get_genes(ids)
Return a dictionary with the genes associated with each condition. 

Parameters:
- ids: List of gene ids or gene labels. 

> **_Note:_** If a given condition is obsolete, it will be added with the _**obsolete**_ property to true and the **_replaced_by_** and **_consider_** properties.

### get_diseases(ids, obsolete_action='replace')
Return a dictionary with the diseases associated with each gene. 

Parameters:
- ids: List of gene ids or gene labels. 
- obsolete_action: Strategy to apply for obsolete conditions.
    - 'show' - obsolete conditions are shown
    - 'hide' - obsolete conditions are removed
    - 'replace' - obsolete conditions are replaced by all terms specify by **_replaced_by_** and **_consider_** properties

> **_Note:_** If a given symptom is obsolete, it will be added with the _**obsolete**_ property to true and the **_replaced_by_** and **_consider_** properties.

## BioPhens Methods

### Ontology

#### all_conds(parent='MONDO:0000001')
Returns a list of all **non-obsolete** conditions children of parameter **_parent_**.

#### all_phens(parent='HP:0000118')
Returns a list of all **non-obsolete** symptoms children of parameter **_parent_**.

#### all_obsolete_conds()
Returns a list of all **obsolete** conditions. Each term include a **_replaced_by_** and **_consider_** properties to determine substitution candidates.

#### all_obsolete_phens()
Returns a list of all **obsolete** symptoms. Each term include a **_replaced_by_** and **_consider_** properties to determine substitution candidates.

#### describe_conds(ids, depth=0, include_obsolete=False)
Returns all information avaliable for each condition term.

Parameters:
- ids: List of term ids
- depth: Level of children to include in the term.
    - depth =-1 - all children are shown
    - depth = 0 - no children are shown
    - depth = N - N level of children are shown
- include_obsolete: Set to True to include obsolete terms

### Successors / Predecessors

#### successors_conds(ids, depth=1)
Returns a dictionary of dictionaries with the succesors for each given condition.

Parameters:
- ids: List of term ids
- depth: Level of children to include in the term.
    - depth =-1 - all children are shown
    - depth = 0 - no children are shown
    - depth = N - N level of children are shown

> **_Note:_** If a given condition is obsolete, it will be shown as an empty dictionary, i.e: 'MONDO:0000002': \{\}

#### successors_phens(ids, depth=1)
Returns a dictionary with the succesors for each given symptom.

Parameters:
- ids: List of term ids
- depth: Level of children to include in the term.
    - depth =-1 - all children are shown
    - depth = 0 - no children are shown
    - depth = N - N level of children are shown

> **_Note:_** If a given symptom is obsolete, it will be shown as an empty dictionary, i.e: 'HP:0000057': \{\}

#### predecessors_conds(ids, depth=1)
Returns a dictionary of dictionaries with the predecesors for each given condition.

Parameters:
- ids: List of term ids
- depth: Level of ancestors to include in the term.
    - depth =-1 - all ancestors are shown
    - depth = 0 - no ancestors are shown
    - depth = N - N level of ancestors are shown

> **_Note:_** If a given condition is obsolete, it will be shown as an empty dictionary, i.e: 'MONDO:0000002': \{\}

#### predecessors_phens(ids, depth=1)
Returns a dictionary with the predecesors for each given symptom.

Parameters:
- ids: List of term ids
- depth: Level of ancestors to include in the term.
    - depth =-1 - all ancestors are shown
    - depth = 0 - no ancestors are shown
    - depth = N - N level of ancestors are shown

> **_Note:_** If a given symptom is obsolete, it will be shown as an empty dictionary, i.e: 'HP:0000057': \{\}


### Describe Terms

#### describe_phens(ids, depth=0, include_obsolete=False)
Returns all information avaliable for each sympton term.

Parameters:
- ids: List of term ids
- depth: Level of children to include in the term.
    - depth =-1 - all children are shown
    - depth = 0 - no children are shown
    - depth = N - N level of children are shown
- include_obsolete: Set to True to include obsolete terms


### Terms Validation

#### validate_conds(ids)
Returns a dictionary with information for each given condition following these rules:

- If the condition is unknown, returns null.
- If the condition is not obsolete, returns the _**obsolete**_ property to false.
- If the condition is obsolete, returns the _**obsolete**_ property to true and the **_replaced_by_** and **_consider_** properties.

#### validate_phens(ids)
Returns a dictionary with information for each given symptom following these rules:

- If the symptom is unknown, returns null.
- If the symptom is not obsolete, returns the _**obsolete**_ property to false.
- If the symptom is obsolete, returns the _**obsolete**_ property to true and the **_replaced_by_** and **_consider_** properties.

### Annotations

#### conditions_phens(ids, obsolete_action='replace')
Given a list of conditions, returns the symptoms annotated for each condition.

Parameters:
- ids: List of condition ids
- obsolete_action: Strategy to apply for obsolete symptoms.
    - 'show' - obsolete symptoms are shown
    - 'hide' - obsolete symptoms are removed
    - 'replace' - obsolete symptoms are replaced by all terms specify by **_replaced_by_** and **_consider_** properties

> **_Note:_** The *obsolete_action* parameter only applies to symptoms, no for given conditions. If a given condition is obsolete, it will has the _**obsolete**_ property to true and include the **_replaced_by_** and **_consider_** properties

#### conditions_phens_recursive(self, ids, depth=-1, obsolete_action='replace')
Same as **_conditions_phens_** but if a condition has children, include same information for each children recursively to depth.

Parameters:
- ids: List of condition ids
- obsolete_action: Strategy to apply for obsolete symptoms.
    - 'show' - obsolete symptoms are shown
    - 'hide' - obsolete symptoms are removed
    - 'replace' - obsolete symptoms are replaced by all terms specify by **_replaced_by_** and **_consider_** properties
- depth: Level of children to include:
    - depth =-1 - all children are shown
    - depth = 0 - no children are shown
    - depth = N - N level of children are shown


### Symptom Groups

#### describe_groups()
Return the list of symptom groups. A symptom group is a HP term children of 'HP:0000118'.

#### group_phens(ids, include_empty=False)
Returns a dictionary with the symptom groups. Each group include a dictionary of items in that group.

Parameters:
- ids: List of symptoms ids
- include_empty: True to return all groups, including groups with no symtoms.

> **_Note:_** If a given symptom is obsolete, it will be added with the _**obsolete**_ property to true and the **_replaced_by_** and **_consider_** properties.


### Misc

#### phen_leaves(dic_phens, depth=-1)
Filter a list of symptoms to show only those who are leaves in the hierarchy. In other words, if a symptom has successors included in the list, that symptom will be removed.

Parameters:
- dic_phens: A dictionary with {'name': <list of symptoms>}
- depth: Level of children to seek:
    - depth =-1 - all children
    - depth = 0 - no children
    - depth = N - N level of children

