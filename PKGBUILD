# Maintainer: Claude Code <noreply@anthropic.com>
pkgname=pdfworks-studio-git
pkgver=1.0.0
pkgrel=1
pkgdesc="Free and Open-Source PDF & Office Document Suite for Linux"
arch=('x86_64')
url="https://github.com/deesspanda/pdfworks-studio"
license=('MIT')
depends=('python' 'python-pyside6' 'python-pymupdf' 'python-pypdf' 'python-pillow')
makedepends=('git' 'python-build' 'python-installer' 'python-wheel')
source=("$pkgname::git+https://github.com/deesspanda/pdfworks-studio.git")
sha256sums=('SKIP')

package() {
    cd "$srcdir/$pkgname"
    install -Dm755 run.sh "$pkgdir/usr/bin/pdfworks-studio"
    install -dm755 "$pkgdir/usr/share/pdfworks-studio"
    cp -r pdfworks_studio "$pkgdir/usr/share/pdfworks-studio/"
    install -Dm644 pdfworks-studio.desktop "$pkgdir/usr/share/applications/pdfworks-studio.desktop"
}
