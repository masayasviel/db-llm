import { sql } from 'drizzle-orm';
import {
  boolean,
  check,
  int,
  mysqlTable,
  text,
  timestamp,
  unique,
  varchar,
} from 'drizzle-orm/mysql-core';

export const User = mysqlTable('user', {
  id: int('id').autoincrement().primaryKey(),
  name: varchar('name', { length: 256 }).notNull(),
  code: varchar('code', { length: 256 }).notNull().unique('uniq_code'),
});

export const Memo = mysqlTable('memo', {
  id: int('id').autoincrement().primaryKey(),
  createdAt: timestamp('created_at', { mode: 'string' }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { mode: 'string' })
    .notNull()
    .defaultNow()
    .onUpdateNow(),
  userId: int('user_id')
    .notNull()
    .references(() => User.id, { onDelete: 'cascade' }),
  title: varchar('title', { length: 256 }).notNull(),
  content: text('content').notNull(),
});

export const Tag = mysqlTable(
  'tag',
  {
    id: int('id').autoincrement().primaryKey(),
    name: varchar('name', { length: 50 }).notNull(),
    isOfficial: boolean('is_official').notNull().default(false),
    userId: int('user_id').references(() => User.id, { onDelete: 'cascade' }),
  },
  (t) => [
    unique('uniq_tag_name').on(t.name, t.isOfficial, t.userId),
    check(
      'check_tag_owner',
      sql`(
        (${t.isOfficial} = TRUE AND ${t.userId} IS NULL)
        OR
        (${t.isOfficial} = FALSE AND ${t.userId} IS NOT NULL)
      )`,
    ),
  ],
);

export const memoTagRelation = mysqlTable('memo_tag_relation', {
  id: int('id').autoincrement().primaryKey(),
  memoId: int('memo_id')
    .notNull()
    .references(() => Memo.id, { onDelete: 'cascade' }),
  tagId: int('tag_id')
    .notNull()
    .references(() => Tag.id, { onDelete: 'cascade' }),
});