const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '', component: () => import('pages/IndexPage.vue')

      },
      {
        path: 'shows',
        component: () => import('pages/ShowsPage.vue'),
        name: 'shows'
      },

      {
        path: 'shows/:id',
        component: () => import('pages/ShowPage.vue'),
        name: 'show'
      },
      {
        path: 'shows/:id/sessions',
        component: () => import('pages/SessionsPage.vue'),
        name: 'sessions'
      },

      {
        path: 'news',
        component: () => import('pages/NewsPage.vue'),
        name: 'news'
      },
      {
        path: 'my-tickets',
        component: () => import('pages/MyTicketsPage.vue'),
        name: 'my-tickets'
      },
      {
        path: 'login',
        component: () => import('pages/LoginPage.vue'),
        name: 'login'
      },
      {
        path: 'actors',
        component: () => import('pages/ActorsPage.vue'),
        name: 'actors'
      },
      {
        path: 'genres',
        component: () => import('pages/GenresPage.vue'),
        name: 'genres'
      },
      {
        path: 'news/:id',
        name: 'news-detail',
        component: () => import('pages/NewsDetail.vue')
      },
       {
        path: 'sessions/:id/seats',
        component: () => import('pages/HallPage.vue'),
        name: 'seats'
      },
      {
        path: 'registration',
        name: 'registration',
        component: () => import('pages/RegistrationPage.vue')
      },
       {
        path: 'profile',
        component: () => import('src/pages/ProfilePage.vue'),
        name: 'profile'
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
