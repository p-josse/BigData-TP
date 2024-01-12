# TP1 Answers

## How many movie have the shop ?

### Query

```SQL
SELECT COUNT(*) AS total_movies FROM film
```

### Result

| total_movies |
|--------------|
| 1000         |

### Explainations

This query will count the number of rows in the `film` table, which indicates the total number of movies available for rent. The `COUNT(*)` function counts the number of rows in a table, and the `AS total_movies` clause gives the result column a descriptive name.


## How many movies are available ?

### Query

```SQL
SELECT COUNT(DISTINCT inventory.film_id) AS available_movies
FROM inventory
```

### Result

| available_movies |
|------------------|
| 958              |

### Explainations

This query selects the `film_id` from the `inventory` table. The `COUNT()` function counts the number of rows in the table. The `DISTINCT` keyword ensures that only one count is included for each unique film. The `AS available_movies` clause provides a descriptive name.


## What is the monthly revenue of the shop ?

### Query

```SQL
SELECT EXTRACT(YEAR FROM rental.rental_date) AS year,
        EXTRACT(MONTH FROM rental.rental_date) AS month,
        SUM(payment.amount) AS total_revenue
FROM rental
JOIN payment ON rental.rental_id = payment.rental_id
GROUP BY year, month;
```

### Result

| year | month | total_revenue |
|------|-------|---------------|
| 2005 | 7 | 28377.87 |
| 2005 | 8 | 24070.14 |
| 2005 | 6 | 8349.85 |
| 2005 | 2 | 514.18 |

### Explainations

- `SELECT`: Specifies the columns that will be included in the output of the query. In this case, the query will select the year, month, and total revenue for each month.
- `EXTRACT(YEAR FROM rental.rental_date)`: This function extracts the year from the `rental_date` column in the `rental` table.
- `EXTRACT(MONTH FROM rental.rental_date)`: This function extracts the month from the `rental_date` column in the `rental` table.
- `SUM(payment.amount)`: This function calculates the sum of the `payment.amount` column for each group of rows. This means that the query will calculate the total revenue for each month.
- `rental.rental_id = payment.rental_id`: This is the join condition, which specifies that the `rental_id` column in the `rental` table must be equal to the `rental_id` column in the `payment` table.
- `GROUP BY year, month`: This clause groups the results by year and month. This means that all of the rows with the same year and month will be grouped together.


## For each client, give the top 3 most viewed movie categories

### Query

```SQL
WITH RankedCategories AS (
  SELECT
    c.customer_id,
    fc.category_id,
    cc.name,
    c.first_name,
    c.last_name,
    ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY COUNT(*) DESC) AS category_rank
  FROM public.customer c
  JOIN public.rental r ON c.customer_id = r.customer_id
  JOIN public.inventory i ON r.inventory_id = i.inventory_id
  JOIN public.film_category fc ON i.film_id = fc.film_id
  JOIN public.category cc ON fc.category_id = cc.category_id
  GROUP BY c.customer_id, fc.category_id, cc.name
)
SELECT
  first_name,
  MAX(CASE WHEN category_rank = 1 THEN name END) AS category1,
  MAX(CASE WHEN category_rank = 2 THEN name END) AS category2,
  MAX(CASE WHEN category_rank = 3 THEN name END) AS category3
FROM RankedCategories
GROUP BY customer_id, first_name
ORDER BY customer_id;
```

### Result

| first_name | category1 | category2 | category3 |
|------------|-----------|-----------|-----------|
| Mary | Classics | Comedy | Drama |
| Patricia | Sports | Classics | Action |
| Linda | Action | Sci-Fi | Animation |
| Barbara | Horror | Foreign | Sci-Fi |
| Elizabeth | Classics | Animation | Family |
| Jennifer | Drama | Children | Sci-Fi |
| Maria | Sports | Animation | New |
| ... | ... | ... | ... |

### Explainations

- Common Table Expression (CTE) - RankedCategories:

    - This part of the query calculates the rank of movie categories for each customer based on the count of movies rented in each category. It uses the `ROW_NUMBER()` window function to assign a rank to each category for each customer.
    - The result includes columns such as `category_id`, `name` (category name), `first_name`, `last_name`, and `category_rank`.

- Main Query:

    - The main query uses the `RankedCategories` CTE and further processes the data to pivot it into a format with four columns: `first_name`, `category1`, `category2`, and `category3`.

- Pivoting with CASE Statements:

    - The `CASE` statements inside the `MAX` function are used for pivoting. Each `CASE` statement checks the `category_rank` and assigns the name (category name) to the corresponding category column (`category1`, `category2`, `category3`).
    - `MAX` function is used to aggregate the values, ensuring that only the relevant category name is selected for each customer and category rank.

- Grouping and Ordering:

    - The result is grouped by `customer_id` and `first_name` to ensure that each row represents a unique customer.
    - The final result set is ordered by `customer_id`.