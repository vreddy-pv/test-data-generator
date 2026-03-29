CREATE TABLE `CATEGORY` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `TRANSACTION` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `description` VARCHAR(255),
    `amount` DECIMAL(19, 2) NOT NULL,
    `date` DATE NOT NULL,
    `category_id` BIGINT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`category_id`) REFERENCES `CATEGORY`(`id`)
);
