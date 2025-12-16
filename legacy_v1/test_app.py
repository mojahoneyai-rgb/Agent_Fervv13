import traceback

try:
    import main
    print("Import successful, creating app...")
    app = main.FervvIDE()
    print("App created successfully!")
    app.mainloop()
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}\n")
    traceback.print_exc()
