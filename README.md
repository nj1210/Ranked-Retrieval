# Information-Retrieval-Assignment

Steps to execute:

Python version above 3.6 required for smooth functioning.

1. Create and Activate virtual environment

```
   $ python3 -m venv ./venv/
   $ source venv/bin/activate
```

2. Install dependencies

```
   $ pip install -r requirements.txt
```

3. Creation of Index

```
   $ cd <MODEL_NAME>
   $ python read.py
```

4. To run the query 

```
   $ cd <MODEL_NAME>
   $ python test_queries.py
```

Trained indexes are already supplied in the file.

Incase you want to print the indexes in readable format, run the following in the folder of the appropriate model:

```
   $ python printIndex.py
```

A file named readable_index.txt is generated in the folder of the appropriate model.
