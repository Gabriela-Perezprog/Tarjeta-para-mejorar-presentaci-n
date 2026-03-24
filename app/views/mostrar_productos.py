import flet as ft 
from typing import Any
from app.services.transacciones_api_productos import list_products, get_product, create_product, update_product, delete_product
from app.components.popup import show_popup, show_popup_auto_close, show_snackbar, confirm_dialog
from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors, Textos, Card

def products_view(page:ft.Page) -> ft.Control: 
    rows_data:list[dict[str,Any]]=[]
    total_items=0 

    total_text = ft.Text("Total de productos: (cargando...)", style=Textos.H3) 

    # Encabezados 
    columnas=[ 
        ft.DataColumn(label=ft.Text("Nombre", style=Textos.H3, color="#1e293b")), 
        ft.DataColumn(label=ft.Text("Cantidad", style=Textos.H3, color="#1e293b")), 
        ft.DataColumn(label=ft.Text("Ingreso", style=Textos.H3, color="#1e293b")), 
        ft.DataColumn(label=ft.Text("Min", style=Textos.H3, color="#1e293b")), 
        ft.DataColumn(label=ft.Text("Max", style=Textos.H3, color="#1e293b")),
    ]

    # Datos de prueba 
    data=[] 
    data.append( 
        ft.DataRow( 
            cells=[ 
                ft.DataCell(ft.Text("nombre1...", color="#334155")), 
                ft.DataCell(ft.Text("cantidad1...", color="#334155")),
                ft.DataCell(ft.Text("ingreso1...", color="#334155")), 
                ft.DataCell(ft.Text("min1...", color="#334155")), 
                ft.DataCell(ft.Text("max1...", color="#334155")),
            ],
            color="#f8fafc"
        )
    )

    # Tabla
    tabla=ft.DataTable( 
        columns=columnas, 
        rows=data, 
        width=900, 
        heading_row_height=60, 
        heading_row_color="#e2e8f0", 
        data_row_max_height=60, 
        data_row_min_height=48,
        border=ft.border.all(1, "#cbd5f5"),
        column_spacing=40
    )

    async def actualizar_data():
        nonlocal rows_data, total_items
        try:
            data=list_products(limit=500, offset=0)
            total_items=int(data.get("total", 0)) 
            total_text.value="Total de productos: "+str(total_items)
            rows_data=data.get("items", []) or []
            actualizar_filas()
        except Exception as ex:
            await show_snackbar(page, "Error al cargar productos: "+str(ex), bgcolor=Colors.DANGER)  
    
    def actualizar_filas():
        nuevas_filas=[]
        for p in rows_data: 
            nuevas_filas.append( 
                ft.DataRow( 
                    cells=[ 
                        ft.DataCell(ft.Text(p.get("name", ""), color="#334155")), 
                        ft.DataCell(ft.Text(str(p.get("quantity", "")), color="#334155")),
                        ft.DataCell(ft.Text(p.get("ingreso_date", ""), color="#334155")), 
                        ft.DataCell(ft.Text(str(p.get("min_stock", "")), color="#334155")), 
                        ft.DataCell(ft.Text(str(p.get("max", "")), color="#334155")),
                    ],
                    color="#f8fafc"
                )
            ) 
        tabla.rows=nuevas_filas
        page.update()

    page.run_task(actualizar_data)

    # SE CREA LA TARJETA
    contenido = ft.Column([
        total_text,
        tabla
    ])

    tarjeta = ft.Container(
        content=contenido,
        **Card.tarjeta
    )

    
    # return tarjeta

    #CONTENEDOR PARA CENTRAR
    final = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, -1),
        content=tarjeta
    )

    return final