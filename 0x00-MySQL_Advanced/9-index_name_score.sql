-- Create an index on a column and a part of a column
Create INDEX idx_name_first_score
ON names(name(1), score);
