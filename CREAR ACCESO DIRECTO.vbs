' ==========================================================
' CREAR ACCESO DIRECTO DE SUPER COMPU BROS (Windows)
'
' Doble click en este archivo: crea "SUPER COMPU BROS" (con el icono del
' juego) en esta carpeta y en el Escritorio. Si moves la carpeta del juego,
' volve a hacerle doble click para que el acceso apunte al lugar nuevo.
' ==========================================================

Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

carpeta = fso.GetParentFolderName(WScript.ScriptFullName)
lanzador = carpeta & "\Super Compu Bros.pyw"
icono = carpeta & "\icono.ico"

' Se busca pythonw.exe (Python sin consola); si no aparece, el acceso
' abre el .pyw directamente
pythonw = ""
nombres = Array("pythonw", "pyw")
For Each nombre In nombres
    If pythonw = "" Then
        On Error Resume Next
        Set busqueda = sh.Exec("cmd /c where " & nombre)
        salida = busqueda.StdOut.ReadAll
        On Error GoTo 0
        lineas = Split(Replace(salida, vbCr, ""), vbLf)
        If UBound(lineas) >= 0 Then
            If Trim(lineas(0)) <> "" And InStr(LCase(lineas(0)), "windowsapps") = 0 Then
                pythonw = Trim(lineas(0))
            End If
        End If
    End If
Next

destinos = Array(carpeta, sh.SpecialFolders("Desktop"))

For Each destino In destinos
    ' Se borra el acceso de antes (con el nombre viejo) y se crea el nuevo
    If fso.FileExists(destino & "\Super Compu Bros.lnk") Then fso.DeleteFile destino & "\Super Compu Bros.lnk"
    Set acceso = sh.CreateShortcut(destino & "\SUPER COMPU BROS.lnk")
    If pythonw <> "" Then
        acceso.TargetPath = pythonw
        acceso.Arguments = """" & lanzador & """"
    Else
        acceso.TargetPath = lanzador
    End If
    acceso.WorkingDirectory = carpeta
    acceso.IconLocation = icono & ",0"
    acceso.Description = "SUPER COMPU BROS"
    acceso.Save
Next

MsgBox "Listo! Se creo el acceso directo ""SUPER COMPU BROS"" en la carpeta del juego y en el Escritorio.", 64, "Super Compu Bros"
