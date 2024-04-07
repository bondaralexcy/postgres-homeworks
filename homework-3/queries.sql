-- Напишите запросы, которые выводят следующую информацию:
-- 1. Название компании заказчика (company_name из табл. customers)
-- и ФИО сотрудника, работающего над заказом этой компании (см таблицу employees),
-- когда и заказчик и сотрудник зарегистрированы в городе London, а доставку заказа ведет компания United Package (company_name в табл shippers)


	select c.company_name, e.FIO from public.orders

	inner join
	(select customer_id, company_name from public.customers where city = 'London') as c
	using (customer_id)

	inner join
	(select employee_id, CONCAT(first_name, ' ', last_name) as FIO from public.employees  where city = 'London') as e
	using (employee_id)

	inner join
	(select shipper_id from public.shippers where company_name = 'United Package') as s
	on orders.ship_via = s.shipper_id;

	-- Но лучше так:

	SELECT customers.company_name as customer, CONCAT(employees.first_name, ' ', employees.last_name) AS emoloyee FROM customers
    JOIN orders USING (customer_id)
    JOIN employees USING (employee_id)
    JOIN shippers ON orders.ship_via = shippers.shipper_id
    WHERE customers.city = 'London' AND employees.city = 'London' AND shippers.company_name = 'United Package';



-- 2. Наименование продукта, количество товара (product_name и units_in_stock в табл products),
-- имя поставщика и его телефон (contact_name и phone в табл suppliers) для таких продуктов,
-- которые не сняты с продажи (поле discontinued) и которых меньше 25 и которые в категориях Dairy Products и Condiments.
-- Отсортировать результат по возрастанию количества оставшегося товара.

select p.product_name, p.units_in_stock, s.contact_name, s.phone
from (
	(select * from public.products
		where products.discontinued <> 1
	 	and products.units_in_stock < 25
	) as p

	inner join
	(select * from public.suppliers) as s
		using (supplier_id)

	inner join
	(select * from public.categories
	 	where category_name in ('Dairy Products', 'Condiments')) as c
		on p.category_id = c.category_id
)
order by p.units_in_stock;

-- Но лучше так:

SELECT product_name, units_in_stock, contact_name, phone FROM products
INNER JOIN suppliers USING (supplier_id)
INNER JOIN categories USING (category_id)
WHERE discontinued = 0 AND units_in_stock < 25 and category_name in('Dairy Products', 'Condiments')
ORDER BY units_in_stock



-- 3. Список компаний заказчиков (company_name из табл customers), не сделавших ни одного заказа

select company_name
from (
	select customer_id, company_name, o.orders_count from public.customers as c

	left join
	(select customer_id, count(order_id) as orders_count from public.orders
		group by customer_id) as o
		using (customer_id)

	where o.orders_count is null
	);

-- Но лучше так:
SELECT company_name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders)

-- 4. уникальные названия продуктов, которых заказано ровно 10 единиц (количество заказанных единиц см в колонке quantity табл order_details)
-- Этот запрос написать именно с использованием подзапроса.

SELECT DISTINCT product_name FROM public.products
WHERE product_id IN (SELECT product_id FROM public.order_details WHERE quantity = 10)
