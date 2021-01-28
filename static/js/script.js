$(document).ready(function (){
    let rows = $('.data_rows')
    
    function drawRow(id){
        let data = '            <div class="data_row row" id="' + id + '">\n' +
            '                        <div class="col-xs-12 col-sm-6 col-md-3">\n' +
            '                            <div class="form-group">\n' +
            '                                <label for="data_rows[' + id + '][name]">Column name</label>\n' +
            '                                <input type="text" class="form-control" name="data_rows[' + id + '][name]" id="data_rows[' + id + '][name]" value="">\n' +
            '                            </div>\n' +
            '                        </div>\n' +
            '                        <div class="col-xs-12 col-sm-6 col-md-3">\n' +
            '                            <div class="form-group">\n' +
            '                                <label for="data_rows[' + id + '][kind]">Separator</label>\n' +
            '                                <select name="data_rows[' + id + '][kind]" id="data_rows[' + id + '][kind]" class="form-control row_kind" data-id="' + id + '">\n' +
            '                                    <option value="name">Full name</option>\n' +
            '                                    <option value="job">Job</option>\n' +
            '                                    <option value="email">E-mail</option>\n' +
            '                                    <option value="domain">Domain name</option>\n' +
            '                                    <option value="phone">Phone number</option>\n' +
            '                                    <option value="company">Company</option>\n' +
            '                                    <option value="text">Text</option>\n' +
            '                                    <option value="int">Integer</option>\n' +
            '                                    <option value="address">Address</option>\n' +
            '                                    <option value="date">Date</option>\n' +
            '                                </select>\n' +
            '                            </div>\n' +
            '                        </div>\n' +
            '                        <div class="col-xs-12 col-sm-6 col-md-3">\n' +
            '                            <div class="row data_counters hidden">\n' +
            '                                <div class="col-xs-6">\n' +
            '                                    <div class="form-group">\n' +
            '                                        <label for="data_rows[' + id + '][start]">From</label>\n' +
            '                                        <input type="number" class="form-control" name="data_rows[' + id + '][start]" id="data_rows[' + id + '][start]" value="">\n' +
            '                                    </div>\n' +
            '                                </div>\n' +
            '                                <div class="col-xs-6">\n' +
            '                                    <div class="form-group">\n' +
            '                                        <label for="data_rows[' + id + '][end]">To</label>\n' +
            '                                        <input type="number" class="form-control" name="data_rows[' + id + '][end]" id="data_rows[' + id + '][end]" value="">\n' +
            '                                    </div>\n' +
            '                                </div>\n' +
            '                            </div>\n' +
            '                        </div>\n' +
            '                        <div class="col-xs-12 col-sm-6 col-md-3">\n' +
            '                            <div class="row">\n' +
            '                                <div class="col-xs-6">\n' +
            '                                    <div class="form-group">\n' +
            '                                        <label for="data_rows[' + id + '][order]">Order</label>\n' +
            '                                        <input type="number" class="form-control" name="data_rows[' + id + '][order]" id="data_rows[' + id + '][order]" value="">\n' +
            '                                    </div>\n' +
            '                                </div>\n' +
            '                                <div class="col-xs-6">\n' +
            '                                    <button type="button" class="btn btn-danger delete_row" data-id="' + id + '">Delete</button>\n' +
            '                                </div>\n' +
            '                            </div>\n' +
            '                        </div>\n' +
            '                    </div>';
        rows.append(data)
        $("#" + id + " input").prop('required', true);
        $("#" + id + " .data_counters input").prop('required', false);
    }
    if (rows){
        let form = $('#data_form')
        let dataJsonInput = $('#data_json')
        drawRow(Date.now())
        rows.on('click', '.delete_row', function (){
            let id = $(this).data('id')
            $("#" + id).remove()
        })
        rows.on('change', '.row_kind', function (){
            let id = $(this).data('id')
            let value = $(this).val()
            if (value === 'text' || value === 'int') {
                $("#" + id + " .data_counters").removeClass('hidden');
                $("#" + id + " .data_counters input").prop('required', true);
            }else {
                $("#" + id + " .data_counters").addClass('hidden')
                $("#" + id + " .data_counters input").prop('required', false);
            }
        })
        $('.add_row').on('click',function (){
            drawRow(Date.now())
        })
        form.on('submit', function (e){
            e.preventDefault()
            let arr = form.serializeArray()
            let data = form.serialize()
            dataJsonInput.val(data)
            form.unbind('submit').submit();
        })
    }
})
