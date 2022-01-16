<script>

</script>

<template>
    <section class="report-wrapper">
        <div class="container">
            <div class="report-main">

                <div class="report-main-first-part">
                    <h3 class="report-main-part-heading">
                        Reports One
                    </h3>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Example select</label>
                                <select class="form-control">
                                    <option>1</option>
                                    <option>2</option>
                                    <option>3</option>
                                    <option>4</option>
                                    <option>5</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label>Product Name</label>
                                        <input class="form-control" list="datalistOptions" id="productName"
                                            placeholder="Type to search...">
                                        <datalist id="datalistOptions">
                                            <option value="San Francisco"/>
                                            <option value="New York"/>
                                            <option value="Seattle"/>
                                            <option value="Los Angeles"/>
                                            <option value="Chicago"/>
                                        </datalist>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label>Example select</label>
                                        <select class="form-control">
                                            <option>1</option>
                                            <option>2</option>
                                            <option>3</option>
                                            <option>4</option>
                                            <option>5</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Start Date</label>
                                <input type="text" class="form-control" id="reportStartDate">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>End Date</label>
                                <input type="text" class="form-control" id="reportEndDate">
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12 text-md-center">
                            <button type="submit" class="btn btn-primary">Genarate Button</button>
                        </div>
                    </div>
                </div>
                <div class="report-print-button text-right">
                    <button type="submit" class="btn btn-success">Print</button>
                </div>
                <div class="report-main-second-part">
                    <h3 class="report-main-part-heading">
                        Reports Two
                    </h3>
                    <div class="report-main-second-part-main">
                        <p><strong>Company Name:</strong>Abc</p>
                        <p><strong>Customer Name:</strong>Abc</p>
                        <p><strong>Start Date:</strong>01-02-2021</p>
                        <p><strong>End Date:</strong>01-02-2021</p>

                        <div class="report-table">
                            <table class="table table-bordered">
                                <thead>
                                    <tr>
                                        <th scope="col">#</th>
                                        <th scope="col">First</th>
                                        <th scope="col">Last</th>
                                        <th scope="col">Handle</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <th scope="row">1</th>
                                        <td>Mark</td>
                                        <td>Otto</td>
                                        <td>@mdo</td>
                                    </tr>
                                    <tr>
                                        <th scope="row">2</th>
                                        <td>Jacob</td>
                                        <td>Thornton</td>
                                        <td>@fat</td>
                                    </tr>
                                    <tr>
                                        <th scope="row">3</th>
                                        <td>Thornton</td>
                                        <td>Larry the Bird</td>
                                        <td>@twitter</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<style>
    .report-main-first-part label {
        margin-bottom: 10px;
    }

    .report-wrapper {
        padding: 50px 0;
    }

    .report-main {
        border: 1px solid #ccc;
        padding: 8px;
    }

    .report-main-part-heading {
        text-align: center;
        margin-bottom: 40px;
    }

    .report-main-first-part,
    .report-main-second-part {
        margin-top: 30px;
        background: linear-gradient(145deg, #e6e6e6, #ffffff);
        box-shadow: 20px 20px 60px #d9d9d9,
            -20px -20px 60px #ffffff;
        padding: 10px;
        border-radius: 5px;
    }

    .report-main-first-part .form-group {
        margin-bottom: 20px;
    }

    .report-print-button {
        margin: 10px 0;
        text-align: right;
    }

    .report-table {
        margin-top: 20px;
    }

    .report-table thead {
        background-color: #ccc;
    }
</style>

