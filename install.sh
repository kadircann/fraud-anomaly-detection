#!/bin/bash

# Anomali Tespit Uygulaması Installer
# Bu script uygulamayı sisteminize kurar

echo "============================================================"
echo "ANOMALİ TESPİT UYGULAMASI KURULUMU"
echo "============================================================"
echo ""

# Kurulum dizini oluştur
INSTALL_DIR="$HOME/Applications/AnomaliTespitUygulamasi"
echo "Kurulum dizini: $INSTALL_DIR"

# Dizin oluştur
mkdir -p "$INSTALL_DIR"

# Dosyaları kopyala
echo "Dosyalar kopyalanıyor..."
cp -r release/* "$INSTALL_DIR/"

# Executable'a çalıştırma izni ver
chmod +x "$INSTALL_DIR/AnomaliTespitUygulamasi"
chmod +x "$INSTALL_DIR/run.sh"

# Desktop'a shortcut oluştur
echo "Desktop shortcut oluşturuluyor..."
cat > "$HOME/Desktop/AnomaliTespitUygulamasi.command" << 'EOF'
#!/bin/bash
cd "$HOME/Applications/AnomaliTespitUygulamasi"
open AnomaliTespitUygulamasi.app
EOF

chmod +x "$HOME/Desktop/AnomaliTespitUygulamasi.command"

echo ""
echo "✅ Kurulum tamamlandı!"
echo ""
echo "Kullanım seçenekleri:"
echo "1. Desktop'taki 'AnomaliTespitUygulamasi.command' dosyasına çift tıklayın"
echo "2. Terminal'den: cd $INSTALL_DIR && open AnomaliTespitUygulamasi.app"
echo "3. Terminal'den: cd $INSTALL_DIR && ./AnomaliTespitUygulamasi"
echo ""
echo "============================================================"
