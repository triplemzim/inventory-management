import { axios } from "@/common/api.service";

export const getCustomerList = async () => {
    const endpoint = '/master/customer-list/';
    try{
        return await axios.get(endpoint);
    } catch (e) {
        console.log(e.response);
        alert(JSON.stringify(e.response.data));
    }
    return {};
}

export const getProductList = async () => {
    const endpoint = '/master/product-list/';
    try{
        return await axios.get(endpoint);
    } catch (e) {
        console.log(e.response);
        alert(JSON.stringify(e.response.data));
    }
    return {};
}

export const getProductListWithBarcode = async (barcode) => {
    const endpoint = '/master/product-barcode/' + barcode + '/';
    try{
        return await axios.get(endpoint);
    } catch (e) {
        console.log(e.response);
        alert(JSON.stringify(e.response.data));
    }
    return {};
}

export const getStockListWithBarcode = async (barcode) => {
    const endpoint = '/master/stocks-list/' + barcode + '/';
    try{
        return await axios.get(endpoint);
    } catch (e) {
        console.log(e.response);
        alert(JSON.stringify(e.response.data));
    }
    return {};
}

export const getWarehouseList = async () => {
    const endpoint = '/master/warehouse-list/';
    try{
        return await axios.get(endpoint);
    } catch (e) {
        console.log(e.response);
        alert(JSON.stringify(e.response.data));
    }
    return {};
}

export const postSale = async (payload) => {
    const endpoint = '/sale/sales/';
    try {
        return await axios.post(endpoint, payload);
    } catch (e) {
        console.log(e.response.data);
        alert(JSON.stringify(e.response.data));
        return e.response;
    }
}
