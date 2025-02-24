SELECT COUNT(*)
FROM (
    SELECT ItemID
    FROM ItemCategory
    GROUP BY ItemID
    HAVING COUNT(Category) = 4
);
