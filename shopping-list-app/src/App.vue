<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    
    <header class="p-3 d-flex justify-content-between align-items-center shadow-sm fixed-top-header"
            style="background-color: #79a38f; color: #fff;">
      <div class="d-flex align-items-center gap-2">
        <span class="fs-3">🛍️</span>
        <h1 class="fs-4 fw-bold mb-0">My Shopping List</h1>
      </div>
      <div class="text-white small text-end">
        {{ currentDate }}<br>{{ currentTime }}
      </div>
    </header>

    <main class="flex-grow-1 p-4 bg-white mt-fixed-header mb-fixed-footer main-content-full-width">
      <h2 class="fw-bold mb-4 d-flex align-items-center gap-2">
        <i class="bi bi-cart-fill"></i> 買い物リスト
      </h2>
      
      <div v-if="items.length === 0" class="alert alert-info text-center" role="alert">
        リストに商品がありません。下のフォームから追加しましょう！
      </div>

      <ul class="list-group shadow-sm">
        <li v-for="item in items" :key="item.id"
            class="list-group-item d-flex justify-content-between align-items-center p-3 mb-2 rounded border-0"
            :class="{'list-group-item-success': item.category === 'Food', 'list-group-item-primary': item.category === 'Household', 'list-group-item-info': item.category === 'Other'}"
        >
          <div class="d-flex align-items-center flex-grow-1 me-3">
            <span class="me-3 fs-5 flex-shrink-0">{{ getCategoryIcon(item.category) }}</span>
            <div class="d-flex flex-column flex-grow-1">
              <span class="fw-bold text-wrap text-break">{{ item.name }}</span>
              <span class="badge bg-secondary rounded-pill mt-1 align-self-start">{{ item.quantity }}個</span>
            </div>
          </div>
          <button @click="deleteItem(item.id)" class="btn btn-danger btn-sm flex-shrink-0">
            <i class="bi bi-trash-fill"></i> 削除
          </button>
        </li>
      </ul>
    </main>

    <footer class="fixed-bottom-footer p-3 bg-dark text-white shadow-lg">
      <div class="footer-content-wrapper d-flex flex-column gap-2">
        <input v-model="newItem.name" type="text" class="form-control form-control-lg" placeholder="商品名を入力" />
        <div class="d-flex gap-2">
          <input v-model.number="newItem.quantity" type="number" class="form-control form-control-lg w-25" placeholder="数量" min="1" />
          <select v-model="newItem.category" class="form-select form-select-lg flex-grow-1">
            <option value="Food">食料品</option>
            <option value="Household">日用品</option>
            <option value="Other">その他</option>
          </select>
        </div>
        <button @click="addItem" class="btn btn-success btn-lg mt-2">
          <i class="bi bi-plus-circle-fill"></i> リストに追加
        </button>
        <button class="btn btn-outline-light text-start w-100 mt-2" @click="alert('設定はまだ未実装です')">
          <i class="bi bi-gear-fill me-2"></i> 設定
        </button>
      </div>
    </footer>
  </div>
</template>

<script>
import api from './api'

export default {
  data() {
    return {
      items: [],
      newItem: {
        name: '',
        quantity: 1,
        category: 'Food'
      },
      currentDate: new Date().toLocaleDateString('ja-JP'),
      currentTime: new Date().toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' })
    }
  },
  async created() {
    try {
      const response = await api.getItems()
      this.items = response.data
    } catch (error) {
      console.error("Failed to fetch items:", error);
      // alert("商品の取得に失敗しました。");
    }
  },
  mounted() {
    this.timer = setInterval(() => {
      this.currentTime = new Date().toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' });
    }, 1000);
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
  methods: {
    async addItem() {
      if (!this.newItem.name.trim()) {
        alert('商品名を入力してください。');
        return;
      }
      try {
        const response = await api.addItem(this.newItem)
        this.items.push(response.data)
        this.newItem = { name: '', quantity: 1, category: 'Food' }
      } catch (error) {
        console.error("Failed to add item:", error);
        alert("商品の追加に失敗しました。");
      }
    },
    async deleteItem(id) {
      if (!confirm('本当にこの商品を削除しますか？')) {
        return;
      }
      try {
        await api.deleteItem(id)
        this.items = this.items.filter(item => item.id !== id)
      } catch (error) {
        console.error("Failed to delete item:", error);
        alert("商品の削除に失敗しました。");
      }
    },
    getCategoryIcon(category) {
      switch (category) {
        case 'Food': return '🍎';
        case 'Household': return '🏠';
        case 'Other': return '📦';
        default: return '🛒';
      }
    }
  }
}
</script>

<style scoped>
/* Bootstrap Iconsのインポート (CDNまたはnpmで導入済みの前提) */
/* @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css"); */

/* 全体のコンテナは既に画面幅いっぱいに広がる設定 */
/* .d-flex.flex-column.min-vh-100.bg-light がルート要素 */

/* bodyとhtmlのデフォルトマージン/パディングをリセットし、親要素が画面全体を占めるようにする */
body, html {
  margin: 0;
  padding: 0;
  min-height: 100%;
  width: 100%; /* これを追加して、bodyとhtmlが横幅いっぱいに広がることを保証 */
  overflow-x: hidden; /* 横スクロールバーが出ないようにする */
  box-sizing: border-box; /* paddingやborderがwidth/heightに含まれるようにする */
}
*, *::before, *::after {
  box-sizing: border-box; /* 全要素にbox-sizingを適用 */
}

.bg-light {
  background-color: #f8f9fa !important;
}

/* 固定ヘッダー */
.fixed-top-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%; /* 画面幅いっぱいに広がる */
  z-index: 1030;
}

/* 固定フッター */
.fixed-bottom-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%; /* 画面幅いっぱいに広がる */
  z-index: 1030;
  display: flex;
  justify-content: center; /* フッター内のコンテンツを中央寄せ */
}

/* フッター内のコンテンツを特定の最大幅に制限するコンテナ */
.footer-content-wrapper {
  max-width: 420px; /* ここでフッター内のコンテンツの幅をスマホサイズに制限 */
  width: 100%; /* 親要素(fixed-bottom-footer)の幅いっぱいに広がる */
}

/* メインコンテンツのパディング調整 (固定ヘッダーとフッターの高さ分) */
.mt-fixed-header {
  margin-top: 75px; /* ヘッダーの高さ + alpha */
}
.mb-fixed-footer {
  margin-bottom: 250px; /* フッターの高さ + alpha */
}

/* 買い物リストの表示領域を常に広げるためのスタイル */
.main-content-full-width {
  width: 100%; 
  /* flex-grow: 1; が適用されているはずだが、念のため flex-basis も指定 */
  flex-basis: auto; /* コンテンツのサイズに基づいて初期サイズを決定 */
  min-width: 0; /* Flexアイテムが縮む際にゼロまで縮めることを許可し、横スクロールを防ぐ */
}

/* ヘッダーの背景色を調整 */
header {
  background-color: #79a38f !important; /* 少し濃いめのグリーン */
}

/* フォーム入力要素の高さとフォントサイズを大きく */
.form-control-lg, .form-select-lg, .btn-lg {
  height: calc(2.8rem + 2px); /* Bootstrapデフォルトより少し大きめ */
  font-size: 1.1rem;
}

/* リストアイテムの背景色と角丸 */
.list-group-item {
  border-radius: 0.5rem !important; /* 少し丸みを帯びる */
  margin-bottom: 0.75rem !important; /* アイテム間の余白 */
  border: 1px solid rgba(0, 0, 0, 0.05) !important; /* 軽いボーダー */
}

/* カテゴリごとの色分けを微調整 (Bootstrapカラーに合わせる) */
.list-group-item-success {
  background-color: #d1e7dd; /* Food */
  color: #0f5132;
}
.list-group-item-primary {
  background-color: #cfe2ff; /* Household */
  color: #052c65;
}
.list-group-item-info {
  background-color: #cff4fc; /* Other */
  color: #055160;
}

/* 商品名と個数の表示調整 */
.list-group-item .fw-bold {
  word-wrap: break-word; /* 長い単語でも折り返す */
  word-break: break-all; /* 単語の途中でも折り返す */
}

/* 個数のバッジ調整 */
.badge {
  font-size: 0.9em; /* 少し大きめ */
  padding: 0.4em 0.8em; /* パディング調整 */
}

/* スクロールバーのデザイン（任意） */
::-webkit-scrollbar {
  width: 0; /* スクロールバーを非表示にする */
  background: transparent; /* 背景も透明に */
}
</style>