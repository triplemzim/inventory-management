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

export default {
  getProductRep,
};
