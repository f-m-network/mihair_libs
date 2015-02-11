<html>
    <head>
        <style type="text/css">
            ${css}
        </style>
    </head>


<body>

    <%
        objs = objects[0]
        lead = leads(objs._id)
    %>

    ${helper.embed_logo_by_name('mihair_sm')|n}
    <table class="header" style="border-bottom: 0px solid black; width: 100%">
            <tr>
                <td style="text-align:right"> </td>
            </tr>
            <tr>
                <td><br/></td>
                <td style="text-align:right"> </td>
            </tr>
            <tr>
                <td>${company.partner_id.name |entity}</td>
                <td/>
            </tr>
            <tr>
                <td >${company.partner_id.street or ''|entity}</td>
                <td/>
            </tr>
            <tr>
                <td>Phone: ${company.partner_id.phone or ''|entity} </td>
                <td/>
            </tr>
            <tr>
                <td>Mail: ${company.partner_id.email or ''|entity}<br/></td>
            </tr>
        </table> ${_debug or ''|n}

    <h2>Contract No: 91723</h2>

    <h3 style="padding-top: 80px">Parties: ${lead.get('partner_id')[1]} and FMN Inc</h3>

    <p style="padding-bottom: 80px">
    Lorem ipsum dolor sit amet, in errem accommodare pri, vim no atomorum
        intellegebat. Cu eos impetus aliquam temporibus, cu per soleat diceret
        temporibus, mea partem impedit an. Sed dico reprehendunt ea, ex per vocent
        hendrerit. Ex nisl reque omnes per, ei eam accusamus corrumpit.
        Graeci suscipiantur mea ei, pri tantas diceret maluisset ei.
        Ea option iracundia deseruisse vim, mel ad liber eloquentiam contentiones.

     Te rebum reprehendunt nec. Cum dolore dicunt eirmod id, homero aliquip
        mei ex. Pro pericula similique ea, ei usu probatus ullamcorper. Ex
        aperiam dissentiunt vim, pro id omnis movet, eirmod postulant referrentur
        duo eu. Per ea soleat omittam commune, id duis maiestatis efficiendi
        eum, pro id inani audiam reprehendunt.
    </p>

    <strong> ___________________ </strong><br>
     ${lead.get('partner_id')[1]}
    <%doc>
    <table width="100%" border="1">
        <tr>
            <td>Name:</td>
            <td>${lead.get('partner_id')[1]}</td>
        </tr>
    </table>
    </%doc>

</body>
</html>
