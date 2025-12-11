const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue')

      },
       { path: 'shows', 
        component: () => import('pages/ShowsPage.vue'),
        name: 'shows'
      },

      { path: 'show/:id', 
        component: () => import('pages/ShowPage.vue'),
        name: 'show'
      },

      { path: 'news', 
        component: () => import('pages/NewsPage.vue'),
        name: 'news'
      },
       { path: '/buy-tickets', 
        component: () => import('pages/BuyTicketsPage.vue'),
        name: 'buy tickets'
      },
      { path: '/my-tickets', 
        component: () => import('pages/MyTicketsPage.vue'),
        name: 'my-tickets'
      },
      { path: '/login', 
        component: () => import('pages/LoginPage.vue'),
        name: 'login'
      },
      { path: '/actors', 
        component: () => import('pages/ActorsPage.vue'),
        name: 'actors'
      },
      { path: '/genres', 
        component: () => import('pages/GenresPage.vue'),
        name: 'genres'
      },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
