import os
from datetime import date
from collections import defaultdict
from PySide6.QtGui import QPainter, QPdfWriter, QPageSize, QPageLayout, QFont, QImage, QColor, QPen, QBrush
from PySide6.QtCore import QSize, QRect, QPoint, Qt
from PySide6.QtWidgets import QWidget

from database.db import SessionLocal
from database.models import Activity, Scelle, Traitement, Tache, KanbanColumn

def export_daily_to_html(filename):
    session = SessionLocal()
    activities = session.query(Activity).all()
    today = date.today()
    
    # Filter for Daily Summary Page logic
    daily_activities = [a for a in activities if a.date == today]
    
    validated_traitements = []
    validated_taches = []
    
    for act in activities:
        for sc in act.scelles:
            for tr in sc.traitements:
                if tr.done and tr.done_at == today:
                    validated_traitements.append(f"{act.name} - Scellé: {sc.name} - {tr.description}")
            for tk in sc.taches:
                if tk.done and tk.done_at == today:
                    validated_taches.append(f"{act.name} - Scellé: {sc.name} - {tk.description}")

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; border-bottom: 2px solid #ddd; padding-bottom: 5px; }}
            .activity {{ margin-bottom: 20px; padding: 10px; background: #f9f9f9; border-left: 4px solid #3498db; }}
            .act-title {{ font-size: 1.2em; font-weight: bold; }}
            .scelle {{ margin-left: 20px; margin-top: 5px; }}
            .status-cta {{ color: green; font-weight: bold; }}
            .status-rep {{ color: orange; font-weight: bold; }}
            .pending {{ color: red; font-size: 0.9em; margin-left: 20px; }}
            .list-item {{ margin: 5px 0; }}
            .check {{ color: green; margin-right: 5px; }}
        </style>
    </head>
    <body>
        <h1>Résumé de la Journée ({today})</h1>
        
        <h2>Activités du jour</h2>
    """
    
    if not daily_activities:
        html += "<p><i>Aucune activité datée d'aujourd'hui.</i></p>"
    else:
        for act in daily_activities:
            html += f"<div class='activity'><div class='act-title'>• {act.name}</div>"
            for s in act.scelles:
                status = []
                if s.cta_validated: status.append("<span class='status-cta'>CTA OK</span>")
                if s.reparations_validated: status.append("<span class='status-rep'>RÉPARATIONS</span>")
                if not status: status.append("En cours")
                status_str = " | ".join(status)
                
                html += f"<div class='scelle'>- Scellé: {s.name} ({status_str})</div>"
                
                pending_t = [t.description for t in s.taches if not t.done]
                pending_tr = [tr.description for tr in s.traitements if not tr.done]
                
                if pending_t:
                    html += f"<div class='pending'>Tâches restantes: {', '.join(pending_t)}</div>"
                if pending_tr:
                    html += f"<div class='pending'>Traitements restants: {', '.join(pending_tr)}</div>"
            html += "</div>"
            
    html += """
        <h2>Actions validées ce jour</h2>
    """
    
    if not validated_traitements and not validated_taches:
        html += "<p><i>Aucune action validée ce jour.</i></p>"
    else:
        if validated_traitements:
            html += "<h3>Traitements</h3>"
            for item in validated_traitements:
                html += f"<div class='list-item'><span class='check'>✔</span> {item}</div>"
                
        if validated_taches:
            html += "<h3>Tâches</h3>"
            for item in validated_taches:
                html += f"<div class='list-item'><span class='check'>✔</span> {item}</div>"
        
    html += """
    </body>
    </html>
    """
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    session.close()
    return True

def export_to_pdf(filename, board_widget):
    writer = QPdfWriter(filename)
    writer.setPageSize(QPageSize.A4)
    writer.setResolution(300) # 300 DPI
    
    painter = QPainter(writer)
    
    session = SessionLocal()
    activities = session.query(Activity).all()
    
    # Page 1: Global Summary Table
    draw_page_1(painter, writer, activities)
    
    # Page 2: Visual Snapshot
    writer.newPage()
    draw_page_2(painter, writer, board_widget)
    
    # Page 3: Charts
    writer.newPage()
    draw_page_3(painter, writer, session)
    
    # Page 4: Daily Summary
    writer.newPage()
    draw_page_4(painter, writer, activities)
    
    session.close()
    painter.end()
    return True

def draw_header(painter, width, title):
    # Draw simple header
    painter.save()
    font = painter.font()
    font.setPointSize(24)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(QRect(0, 0, width, 100), Qt.AlignCenter, title)
    painter.restore()

def draw_page_1(painter, writer, activities):
    page_rect = writer.pageLayout().paintRectPixels(writer.resolution())
    width = page_rect.width()
    
    draw_header(painter, width, "Récapitulatif Global")
    
    # Table settings
    y = 150
    row_height = 80
    col_widths = [300, 800, 400, 800] # Date, Name, Column, Scelles
    headers = ["Date", "Nom", "Colonne", "Scellés"]
    
    painter.save()
    font = painter.font()
    font.setPointSize(10)
    painter.setFont(font)
    
    # Draw Headers
    x = 50
    painter.setBrush(QColor("#f2f2f2"))
    painter.setPen(Qt.black)
    
    for i, h in enumerate(headers):
        rect = QRect(x, y, col_widths[i], row_height)
        painter.drawRect(rect)
        painter.drawText(rect, Qt.AlignCenter, h)
        x += col_widths[i]
        
    y += row_height
    
    # Draw Rows (limit lines to fit page for simplicity, or just truncate)
    # Ideally should handle pagination for table, but requirement says "Page 1 is table"
    # We will fill Page 1 and stop if full.
    
    font.setBold(False)
    painter.setFont(font)
    
    for act in activities:
        if y + row_height > page_rect.height() - 50:
            break # Stop if page full
            
        x = 50
        
        # Date
        painter.drawText(QRect(x + 10, y, col_widths[0] - 20, row_height), Qt.AlignVCenter | Qt.AlignLeft, str(act.date))
        painter.drawRect(QRect(x, y, col_widths[0], row_height))
        x += col_widths[0]
        
        # Name
        painter.drawText(QRect(x + 10, y, col_widths[1] - 20, row_height), Qt.AlignVCenter | Qt.AlignLeft, act.name)
        painter.drawRect(QRect(x, y, col_widths[1], row_height))
        x += col_widths[1]
        
        # Column
        col_name = act.column.name if act.column else "N/A"
        painter.drawText(QRect(x + 10, y, col_widths[2] - 20, row_height), Qt.AlignVCenter | Qt.AlignLeft, col_name)
        painter.drawRect(QRect(x, y, col_widths[2], row_height))
        x += col_widths[2]
        
        # Scelles
        scelles_str = ", ".join([s.name for s in act.scelles])
        # Text ellipsis if too long
        painter.drawText(QRect(x + 10, y, col_widths[3] - 20, row_height), Qt.AlignVCenter | Qt.AlignLeft, scelles_str)
        painter.drawRect(QRect(x, y, col_widths[3], row_height))
        
        y += row_height

    painter.restore()

def draw_page_2(painter, writer, board_widget):
    page_rect = writer.pageLayout().paintRectPixels(writer.resolution())
    width = page_rect.width()
    height = page_rect.height()
    
    draw_header(painter, width, "Vue du Programme")
    
    # Capture board
    # Ensure board is laid out
    # Grab the viewport of the scroll area to get the full content if possible, 
    # but board_widget passed in might be the ScrollArea itself. 
    # We want the content widget.
    
    target_widget = board_widget.widget() if hasattr(board_widget, "widget") else board_widget
    
    # We force the widget to render fully even if hidden/scrolled
    # Use render()
    
    pixmap = target_widget.grab()
    image = pixmap.toImage()
    
    # Scale to fit page
    available_w = width - 100
    available_h = height - 200 # Space for header
    
    scaled_image = image.scaled(QSize(available_w, available_h), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    x = 50
    y = 150
    painter.drawImage(x, y, scaled_image)

def draw_page_3(painter, writer, session):
    page_rect = writer.pageLayout().paintRectPixels(writer.resolution())
    width = page_rect.width()
    
    draw_header(painter, width, "Statistiques")
    
    # 1. Activities per Column Bar Chart
    columns = session.query(KanbanColumn).all()
    col_counts = {}
    max_count = 0
    for col in columns:
        c = len(col.activities)
        col_counts[col.name] = c
        if c > max_count: max_count = c
    
    if max_count == 0: max_count = 1
    
    # Draw Bar Chart
    y = 200
    painter.drawText(50, y, "Activités par Colonne")
    y += 50
    
    bar_height = 500
    chart_width = width - 200
    bar_width = chart_width / len(columns) if columns else chart_width
    
    x = 100
    
    painter.save()
    painter.setPen(Qt.black)
    
    # Draw Axis
    painter.drawLine(x, y + bar_height, x + chart_width, y + bar_height) # X
    painter.drawLine(x, y, x, y + bar_height) # Y
    
    for i, col in enumerate(columns):
        count = col_counts[col.name]
        h = (count / max_count) * bar_height
        
        bar_rect = QRect(x + (i * bar_width) + 10, y + bar_height - h, bar_width - 20, h)
        
        painter.setBrush(QColor("#4CAF50")) # Green bars
        painter.drawRect(bar_rect)
        
        # Label
        painter.drawText(QRect(x + (i * bar_width), y + bar_height + 10, bar_width, 50), Qt.AlignCenter | Qt.TextWordWrap, col.name)
        # Count
        painter.drawText(QRect(x + (i * bar_width), y + bar_height - h - 30, bar_width, 30), Qt.AlignCenter, str(count))
        
    painter.restore()
    
    # 2. Global Task/Traitement Completion
    y += bar_height + 150
    painter.drawText(50, y, "Progression Globale (Tâches + Traitements)")
    y += 50
    
    total_taches = session.query(Tache).count()
    done_taches = session.query(Tache).filter(Tache.done == True).count()
    
    total_trait = session.query(Traitement).count()
    done_trait = session.query(Traitement).filter(Traitement.done == True).count()
    
    total_items = total_taches + total_trait
    total_done = done_taches + done_trait
    
    if total_items > 0:
        pct = (total_done / total_items)
        pie_size = 400
        pie_rect = QRect(width/2 - pie_size/2, y, pie_size, pie_size)
        
        painter.save()
        painter.setBrush(QColor("#ddd"))
        painter.drawPie(pie_rect, 0, 16 * 360) # Full circle
        
        painter.setBrush(QColor("#2196F3")) # Blue
        painter.drawPie(pie_rect, 90 * 16, -int(pct * 360 * 16)) # Done slice (negative for clockwise)
        
        # Legend
        painter.setBrush(Qt.NoBrush)
        painter.drawText(pie_rect, Qt.AlignCenter, f"{int(pct*100)}%")
        painter.restore()
        
        # Legend Text
        painter.drawText(width/2 + pie_size/2 + 50, y + 50, f"Total: {total_items}")
        painter.drawText(width/2 + pie_size/2 + 50, y + 100, f"Fait: {total_done}")

def draw_page_4(painter, writer, activities):
    page_rect = writer.pageLayout().paintRectPixels(writer.resolution())
    width = page_rect.width()
    
    today = date.today()
    draw_header(painter, width, f"Résumé de la Journée ({today})")
    
    daily_activities = [a for a in activities if a.date == today]
    
    y = 200
    x = 100
    
    painter.save()
    font = painter.font()
    
    if not daily_activities:
        font.setPointSize(14)
        font.setItalic(True)
        painter.setFont(font)
        painter.drawText(QRect(x, y, width - 200, 100), Qt.AlignCenter, "Aucune activité datée d'aujourd'hui.")
    else:
        for act in daily_activities:
            # Activity container
            painter.setPen(Qt.black)
            painter.setBrush(Qt.NoBrush)
            
            font.setPointSize(12)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(x, y, f"• {act.name}")
            y += 40
            
            font.setPointSize(10)
            font.setBold(False)
            painter.setFont(font)
            
            # Details: Scellés status
            for s in act.scelles:
                status = []
                if s.cta_validated: status.append("CTA OK")
                if s.reparations_validated: status.append("RÉPARATIONS")
                if not status: status.append("En cours")
                
                status_str = " | ".join(status)
                painter.drawText(x + 30, y, f"- Scellé: {s.name} ({status_str})")
                y += 30
                
                # Pending items
                pending_t = [t.description for t in s.taches if not t.done]
                pending_tr = [tr.description for tr in s.traitements if not tr.done]
                
                if pending_t:
                    painter.setPen(QColor("red"))
                    painter.drawText(x + 60, y, f"Tâches restantes: {', '.join(pending_t)}")
                    y += 30
                if pending_tr:
                    painter.setPen(QColor("orange"))
                    painter.drawText(x + 60, y, f"Traitements restants: {', '.join(pending_tr)}")
                    y += 30
                    
            y += 20 # Spacing
            painter.setPen(Qt.black)
            
    painter.restore()

    # --- Section: Traitements & Taches Validés ce jour ---
    y += 50
    if y > page_rect.height() - 200: # New Page if needed
        writer.newPage()
        y = 100
    
    painter.save()
    font = painter.font()
    font.setPointSize(14)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(QRect(50, y, width, 50), Qt.AlignLeft, "Actions validées ce jour")
    y += 60
    
    # Fetch from DB logic or filter from activities (Activities might not have everything loaded if closed session, 
    # but we queried all activities. relations are lazy loaded usually, but here we can traverse.)
    # Optimally we query directly, but we don't have session passed to this function.
    # However we passed session to draw_page_3, we should have passed it here too or open new one.
    # Actually draw_page_4 receives activities list.
    # We can iterate all activities -> scelles -> items.
    
    validated_traitements = []
    validated_taches = []
    
    for act in activities:
        for sc in act.scelles:
            for tr in sc.traitements:
                if tr.done and tr.done_at == today:
                    validated_traitements.append(f"{act.name} - Scellé: {sc.name} - {tr.description}")
            for tk in sc.taches:
                if tk.done and tk.done_at == today:
                    validated_taches.append(f"{act.name} - Scellé: {sc.name} - {tk.description}")

    font.setPointSize(12)
    font.setBold(True)
    painter.setFont(font)
    
    x = 100
    
    # Traitements
    painter.setPen(QColor("#2E7D32")) # Green
    painter.drawText(x, y, f"Traitements ({len(validated_traitements)})")
    y += 30
    
    font.setPointSize(10)
    font.setBold(False)
    painter.setFont(font)
    painter.setPen(Qt.black)
    
    if not validated_traitements:
         painter.drawText(x + 20, y, "- Aucun")
         y += 20
    else:
        for item in validated_traitements:
            painter.drawText(x + 20, y, f"✔ {item}")
            y += 20
            
    y += 30
    
    # Taches
    font.setPointSize(12)
    font.setBold(True)
    painter.setFont(font)
    painter.setPen(QColor("#1565C0")) # Blue
    painter.drawText(x, y, f"Tâches ({len(validated_taches)})")
    y += 30
    
    font.setPointSize(10)
    font.setBold(False)
    painter.setFont(font)
    painter.setPen(Qt.black)
    
    if not validated_taches:
         painter.drawText(x + 20, y, "- Aucune")
         y += 20
    else:
        for item in validated_taches:
            painter.drawText(x + 20, y, f"✔ {item}")
            y += 20

    painter.restore()
