# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data'), ('config', 'config'), ('models', 'models'), ('services', 'services'), ('utils', 'utils')],
    hiddenimports=['tkinter', 'tkinter.ttk', 'matplotlib.backends.backend_tkagg', 'sklearn.ensemble', 'sklearn.svm', 'sklearn.preprocessing', 'sklearn.model_selection', 'sklearn.metrics', 'sklearn.decomposition'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AnomaliTespitUygulamasi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='AnomaliTespitUygulamasi.app',
    icon=None,
    bundle_identifier=None,
)
