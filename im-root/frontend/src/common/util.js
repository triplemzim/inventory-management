const separator = " - ";
const getProductRep = (product) => {
    return (
        product.brand.name +
        separator +
        product.name +
        separator +
        product.category.name
    );
};

const getSalesmanRep = (salesman) => {
    return (
        salesman.name +
        separator +
        salesman.custom_id
    )
}

const getSalesmanName = (salesman) => {
    return salesman.split('-')[0].trim();
}

export default {
    getProductRep,
    getSalesmanRep,
    getSalesmanName,
};
