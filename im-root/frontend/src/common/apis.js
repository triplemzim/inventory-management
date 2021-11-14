import { axios } from "@/common/api.service";

export const getCustomerList = async () => {
    const endpoint = '/master/customer-list/';
    try{
        return await axios.get(endpoint)
    } catch (e) {
        console.log(e.response);
        alert(e.response.statusText);
    }
    return {};
}

export const getProductList = async () => {
    const endpoint = '/master/product-list/';
    try{
        return await axios.get(endpoint)
    } catch (e) {
        console.log(e.response);
        alert(e.response.statusText);
    }
    return {};
}

export const getProductListWithBarcode = async (barcode) => {
    const endpoint = '/master/product-barcode/' + barcode + '/';
    try{
        return await axios.get(endpoint)
    } catch (e) {
        console.log(e.response);
        alert(e.response.statusText);
    }
    return {};
}

export const getStockListWithBarcode = async (barcode) => {
    const endpoint = '/master/stocks-list/' + barcode + '/';
    try{
        return await axios.get(endpoint)
    } catch (e) {
        console.log(e.response);
        alert(e.response.statusText);
    }
    return {};
}
