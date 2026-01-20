import { sql } from 'drizzle-orm';
import {
  boolean,
  check,
  int,
  mysqlTable,
  text,
  timestamp,
  varchar,
} from 'drizzle-orm/mysql-core';

/** ユーザ */
export const User = mysqlTable('user', {
  id: int('id').autoincrement().primaryKey(),
  /** ユーザ名 */
  name: varchar('name', { length: 256 }).notNull(),
  /** ユーザコード */
  code: varchar('code', { length: 256 }).notNull().unique('uniq_code'),
});

/** メモ */
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
  /** タイトル */
  title: varchar('title', { length: 256 }).notNull(),
  /** 内容 */
  content: text('content').notNull(),
});

/** タグ */
export const Tag = mysqlTable(
  'tag',
  {
    id: int('id').autoincrement().primaryKey(),
    /** タグ名 */
    name: varchar('name', { length: 50 }).notNull(),
    /** 公式タグか */
    isOfficial: boolean('is_official').notNull().default(false),
    userId: int('user_id').references(() => User.id, { onDelete: 'cascade' }),
  },
  (t) => [
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

/** タグ-メモ関連付け */
export const memoTagRelation = mysqlTable('memo_tag_relation', {
  id: int('id').autoincrement().primaryKey(),
  memoId: int('memo_id')
    .notNull()
    .references(() => Memo.id, { onDelete: 'cascade' }),
  tagId: int('tag_id')
    .notNull()
    .references(() => Tag.id, { onDelete: 'cascade' }),
});