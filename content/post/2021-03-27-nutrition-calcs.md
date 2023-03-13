
#### Trying to figure out whether Calories specified typically include grams from Fiber

* Managed to find some documentation , [here](https://fdc.nal.usda.gov/docs/Foundation_Foods_Documentation_Oct2020.pdf) on "proximates" ,

> "Carbohydrate content, referred to as “carbohydrate by difference” in the tables, is expressed as the difference between 100 and the sum of the percentages of water, protein, total lipid (fat), ash, and alcohol (when present). Values for carbohydrate by difference include total dietary fiber content. “Sugars, total NLEA” refers to the sum of the values for individual monosaccharides (galactose, glucose, and fructose) and disaccharides (sucrose, lactose, and maltose), which are those sugars analyzed for nutrition labelling. Because the analyses of total dietary fiber, total sugars, and starch content are conducted separately and reflect the analytical variability inherent in the measurement process, the sum of these carbohydrate fractions may not equal the carbohydrate-by-difference value or may even exceed it."

* As for energy,

> "Food energy is expressed in kcal and is no longer expressed in kJ as of October 2020. The data represent physiologically available energy, which is the value remaining after digestive and urinary losses are deducted from gross energy (Merrill and Watt, 1973).Energy values are calculated when fat and protein values are available for a food."

> "Most energy values are calculated using the Atwater general factors of 4, 9, and 4 for protein, fat, and carbohydrates, respectively. These general calculations are represented in FoodData Central as “Metabolizable Energy (Atwater General Factor)” and is identified in download files and API with nutrient ID: 2047. "

* I think at least based on looking at [macadamia nuts data](https://nutritiondata.self.com/facts/nut-and-seed-products/3123/2) which is basically also from NAL USDA, I think the answer is yes, the calculated "total calories" is from total carbs, which includes fiber grams.
